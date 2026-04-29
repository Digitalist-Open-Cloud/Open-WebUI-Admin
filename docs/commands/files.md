# Files Commands

Manage files in your Open WebUI instance. Files can be uploaded, organized into knowledge bases, and used for RAG (Retrieval-Augmented Generation).

## Commands Overview

| Command | Description |
|---------|-------------|
| `files list` | List all files |
| `files show <id>` | Show file details |
| `files upload <path>` | Upload a file |
| `files delete <id>` | Delete a file |

## List Files

List all files in your Open WebUI instance:

```bash
open-webui-admin files list
```

Output:
```
file-001  document.pdf (102400 bytes)
file-002  image.png (51200 bytes)
file-003  data.csv (2048 bytes)
```

If no files exist:
```
No files
```

## Show File Details

Show detailed information about a specific file:

```bash
open-webui-admin files show file-001
```

Output:
```
ID: file-001
Name: document.pdf
Size: 102400 bytes
Type: application/pdf
```

If the file is not found:
```
File 'nonexistent' not found
```

## Upload File

Upload a file to Open WebUI:

```bash
open-webui-admin files upload /path/to/document.pdf
```

Output:
```
Uploaded: document.pdf -> file-001
```

### Specify MIME Type

If automatic MIME type detection fails, specify it manually:

```bash
open-webui-admin files upload /path/to/file --mime-type "application/pdf"
```

Common MIME types:
- `application/pdf` - PDF documents
- `text/plain` - Plain text files
- `text/csv` - CSV data files
- `image/png` - PNG images
- `image/jpeg` - JPEG images

## Delete File

Delete a file from Open WebUI:

```bash
open-webui-admin files delete file-001
```

Output:
```
Deleted: file-001
```

**Warning**: This permanently deletes the file. If the file is referenced by knowledge bases, use `knowledge remove-file` first to unlink it.

## Workflow Example

A typical workflow for managing files:

```bash
# 1. Upload multiple files
open-webui-admin files upload /path/to/doc1.pdf
open-webui-admin files upload /path/to/doc2.txt
open-webui-admin files upload /path/to/data.csv

# 2. List all files to get their IDs
open-webui-admin files list

# 3. Show details of a specific file
open-webui-admin files show file-001

# 4. Create a knowledge base and add files
open-webui-admin knowledge create --name "My Research"
open-webui-admin knowledge add-file kb-001 file-001
open-webui-admin knowledge add-file kb-001 file-002

# 5. Verify files are in the knowledge base
open-webui-admin knowledge files kb-001

# 6. When done, clean up
open-webui-admin knowledge remove-file kb-001 file-001
open-webui-admin files delete file-001
```

## File Storage

Files uploaded to Open WebUI are:
- Stored on the server's filesystem or object storage
- Accessible via the API using their file ID
- Usable in knowledge bases for RAG
- Referenced by their unique ID (format: `file-xxx`)

## API Endpoints Used

| Command | Endpoint |
|---------|-----------|
| `list` | `GET /api/v1/files/` |
| `show` | `GET /api/v1/files/{id}` |
| `upload` | `POST /api/v1/files/` (multipart/form-data) |
| `delete` | `DELETE /api/v1/files/{id}` |

## Notes

- File uploads use `multipart/form-data` encoding
- MIME type is auto-detected from file extension using Python's `mimetypes` module
- File size is reported in bytes
- Deleting a file that's in use by a knowledge base may cause issues - always remove from knowledge bases first
