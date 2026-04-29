# Knowledge Commands

Manage knowledge bases in your Open WebUI instance. Knowledge bases store documents that can be used for RAG (Retrieval-Augmented Generation) with models.

## Commands Overview

| Command | Description |
|---------|-------------|
| `knowledge list` | List all knowledge bases |
| `knowledge show <id>` | Show knowledge base details |
| `knowledge files <id>` | List files in a knowledge base |
| `knowledge create --name <name>` | Create a new knowledge base |
| `knowledge delete <id>` | Delete a knowledge base |
| `knowledge add-file <id> <file-id>` | Add a file to a knowledge base |
| `knowledge remove-file <id> <file-id>` | Remove a file from a knowledge base |
| `knowledge add-folder <id> <folder>` | Upload all files from folder to KB |

## List Knowledge Bases

List all knowledge bases in your instance:

```bash
open-webui-admin knowledge list
```

Output:
```
kb-001  My Knowledge Base
kb-002  Research Documents
kb-003  Technical Docs
```

## Show Knowledge Base Details

Show detailed information about a specific knowledge base:

```bash
open-webui-admin knowledge show kb-001
```

Output:
```
ID: kb-001
Name: My Knowledge Base
Description: A collection of technical documents
Grants: 2
```

## List Files in Knowledge Base

List all files stored in a knowledge base:

```bash
open-webui-admin knowledge files kb-001
```

Output:
```
file-001  document1.pdf
file-002  report.txt
file-003  data.csv
```

If the knowledge base is not found:
```
Knowledge base 'nonexistent' not found
```

## Create Knowledge Base

Create a new knowledge base:

```bash
open-webui-admin knowledge create --name "Research Docs" --description "Academic papers and references"
```

Output:
```
Created: kb-004
```

Options:
- `--name` (required): Name of the knowledge base
- `--description`: Optional description (default: empty)

## Delete Knowledge Base

Delete a knowledge base:

```bash
open-webui-admin knowledge delete kb-001
```

Output:
```
Deleted: kb-001
```

**Warning**: This only deletes the knowledge base container. Files must be removed separately using `knowledge remove-file` or deleted via the files commands.

## Add File to Knowledge Base

Add an existing file to a knowledge base:

```bash
open-webui-admin knowledge add-file kb-001 file-001
```

Output:
```
Added file-001 to kb-001
```

The file must already be uploaded to Open WebUI (see `files upload` command).

## Add Folder to Knowledge Base

Upload all files from a local folder and add them to a knowledge base in one command:

```bash
open-webui-admin knowledge add-folder <id> /path/to/folder
```

Output:
```
Found 5 file(s) to upload...
  Uploading document1.pdf... done
  Uploading document2.pdf... done
  Uploading notes.txt... done
  Uploading data.csv... done
  Uploading image.png... done

Summary: 5 uploaded, 0 failed

Uploaded files:
  document1.pdf -> file-001
  document2.pdf -> file-002
  notes.txt -> file-003
  data.csv -> file-004
  image.png -> file-005
```

### Pattern Matching

Only upload files matching a specific pattern:

```bash
# Only PDF files
open-webui-admin knowledge add-folder kb-001 /path/to/folder --pattern "*.pdf"

# Only text files
open-webui-admin knowledge add-folder kb-001 /path/to/folder --pattern "*.txt"
```

### Recursive Upload

Upload files from subfolders as well:

```bash
open-webui-admin knowledge add-folder kb-001 /path/to/folder --recursive
```

### Combined Options

```bash
# Recursively upload only PDF files
open-webui-admin knowledge add-folder kb-001 /path/to/folder --recursive --pattern "*.pdf"
```

## Remove File from Knowledge Base

Remove a file from a knowledge base:

```bash
open-webui-admin knowledge remove-file kb-001 file-001
```

Output:
```
Removed file-001 from kb-001 (file destroyed)
```

**Warning**: This permanently deletes the file from Open WebUI, not just from the knowledge base.

## Workflow Example

### Manual File Upload

A typical workflow for setting up a knowledge base with individual files:

```bash
# 1. Upload documents
open-webui-admin files upload /path/to/document.pdf
# Output: Uploaded: document.pdf -> file-001

# 2. Create knowledge base
open-webui-admin knowledge create --name "My Docs" --description "Important documents"

# 3. Add file to knowledge base
open-webui-admin knowledge add-file kb-001 file-001

# 4. Verify files are in the knowledge base
open-webui-admin knowledge files kb-001

# 5. Later, remove a file (destroys the file)
open-webui-admin knowledge remove-file kb-001 file-001
```

### Batch Upload with add-folder

Quickly upload an entire folder of documents:

```bash
# 1. Create knowledge base
open-webui-admin knowledge create --name "Research Papers"

# 2. Upload all PDFs from a folder
open-webui-admin knowledge add-folder kb-002 /path/to/papers --pattern "*.pdf"

# 3. Recursively upload all files from subfolders
open-webui-admin knowledge add-folder kb-002 /path/to/documents --recursive

# 4. Verify all files were added
open-webui-admin knowledge files kb-002
```

## API Endpoints Used

| Command | Endpoint |
|---------|-----------|
| `list` | `GET /api/v1/knowledge/` |
| `show` | `GET /api/v1/knowledge/{id}` |
| `files` | `GET /api/v1/knowledge/{id}/files` |
| `create` | `POST /api/v1/knowledge/create` |
| `delete` | `DELETE /api/v1/knowledge/{id}/delete` |
| `add-file` | `POST /api/v1/knowledge/{id}/file/add` |
| `remove-file` | `POST /api/v1/knowledge/{id}/file/remove` |
| `add-folder` | `POST /api/v1/files/` + `POST /api/v1/knowledge/{id}/file/add` |
