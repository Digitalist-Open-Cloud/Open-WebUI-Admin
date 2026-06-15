import click
from .client import get_client
from .output import print_json, print_success, print_error, die


@click.group("tika")
def tika():
    """Test Tika file processing integration."""
    pass


@tika.command("test")
@click.option("--path", "-p", "file_path", help="PDF file to upload and process for testing")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def tika_test(file_path, json_output):
    """Upload a PDF file and test the Tika processing pipeline via the Open WebUI API."""
    if not file_path:
        import os
        default_path = os.path.join(os.getcwd(), "test-artifacts", "tika-test.pdf")
        if os.path.exists(default_path):
            file_path = default_path

    if not file_path:
        msg = "No file provided. Use --path to specify a file, or place a PDF at test-artifacts/tika-test.pdf"
        if json_output:
            print_json({"result": "error", "error": msg})
        else:
            click.echo(msg, err=True)
        return

    import os
    if not os.path.exists(file_path):
        msg = f"File not found: {file_path}"
        if json_output:
            print_json({"result": "error", "error": msg})
        else:
            click.echo(msg, err=True)
        return

    filename = file_path.rsplit("/", 1)[-1]
    file_id = None
    steps = {}

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Step 1: Upload
    upload_ok = False
    with get_client() as client:
        try:
            resp = client.post(
                "/api/v1/files/",
                files={"file": (filename, file_data, "application/pdf")},
                params={"process": True, "process_in_background": True},
            )
            resp.raise_for_status()
            file_info = resp.json()
            file_id = file_info.get("id", file_info.get("file_id"))
            upload_ok = True
            if not json_output:
                click.echo(f"[1/4] Uploaded '{filename}' -> id: {file_id}")
            steps["upload"] = {"status": "success", "file_id": file_id}
        except Exception as e:
            steps["upload"] = {"status": "fail", "error": str(e)}
            if not json_output:
                click.echo(f"[1/4] Upload failed: {e}", err=True)

    if not upload_ok or not file_id:
        result = "fail"
        _print_tika_result(result, file_id, steps, json_output=json_output)
        return

    # Step 2: Poll processing status
    process_ok = False
    process_result = {}
    with get_client() as client:
        for attempt in range(10):
            try:
                resp = client.get(f"/api/v1/files/{file_id}/process/status")
                resp.raise_for_status()
                status_data = resp.json()
                status = str(status_data).upper()

                if "SUCCESS" in status or "done" in status.lower() or "completed" in status.lower():
                    process_ok = True
                    if not json_output:
                        click.echo(f"[2/4] Processing complete (attempt {attempt + 1})")
                    process_result = status_data
                    break
                elif "FAIL" in status or "error" in status.lower() or "reject" in status.lower():
                    if not json_output:
                        click.echo(f"[2/4] Processing failed: {status_data.get('status', status_data)}", err=True)
                    process_result = status_data
                    break
                else:
                    if not json_output:
                        click.echo(f"[2/4] Processing... (attempt {attempt + 1}/10, status: {status_data.get('status', status_data)})")
                    import time
                    time.sleep(2)
            except Exception as e:
                process_result = {"error": str(e)}
                if not json_output:
                    click.echo(f"[2/4] Status check failed: {e}", err=True)
                break

        steps["processing"] = {
            "status": "success" if process_ok else "fail",
            "result": process_result,
        }

    if not process_ok:
        result = "fail"
        _print_tika_result(result, file_id, steps, json_output=json_output)
        return

    # Step 3: Retrieve processed content
    content_ok = False
    content_length = 0
    content_text = ""
    with get_client() as client:
        try:
            resp = client.get(f"/api/v1/files/{file_id}/data/content")
            resp.raise_for_status()
            content = resp.text
            content_text = content
            content_length = len(content)
            content_ok = True
            if not json_output:
                click.echo(f"[3/4] Retrieved content: {content_length} chars")
        except Exception as e:
            if not json_output:
                click.echo(f"[3/4] Content retrieval failed: {e}", err=True)
            steps["content"] = {"status": "fail", "error": str(e)}
            result = "fail"
            _print_tika_result(result, file_id, steps, json_output)
            return

    steps["content"] = {"status": "success", "content_length": content_length}

    # Step 4: Verify content is meaningful
    content_ok = content_length > 10
    if content_ok:
        result = "success"
    else:
        result = "fail"
        if not json_output:
            click.echo(f"[4/4] Content too short ({content_length} chars)", err=True)

    steps["verification"] = {"status": "ok" if content_ok else "fail", "content_length": content_length}

    _print_tika_result(result, file_id, steps, content_text, json_output)



def _print_tika_result(result, file_id, steps, content_text=None, json_output=False):
    """Print the Tika test result."""
    result_data = {
        "result": result,
        "file_id": file_id,
        "steps": steps,
    }
    if json_output:
        print_json(result_data)
        return

    if result == "success":
        print_success("\n=== Tika test: PASSED ===")
        click.echo(f"File ID: {file_id}")
        for step_name, step_data in steps.items():
            status = step_data.get("status", "unknown")
            icon = "OK" if status == "success" else status.upper()
            click.echo(f"  [{icon}] {step_name}")

        content_length = steps.get("content", {}).get("content_length", 0)
        if content_text:
            click.echo(f"\nExtracted content ({content_length} chars):\n{content_text}")
    else:
        print_error("\n=== Tika test: FAILED ===")
        for step_name, step_data in steps.items():
            status = step_data.get("status", "unknown")
            icon = "OK" if status == "success" else status.upper()
            click.echo(f"  [{icon}] {step_name}")
            if step_data.get("error"):
                click.echo(f"      Error: {step_data['error']}")
