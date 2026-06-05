from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


# Write a tool to read a doc
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of documents and return it as a string."
)
def read_document(
        doc_id: str = Field(description="ID of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} does not exist")
    return docs[doc_id]


# Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document content with a new string"
)
def edit_document(
        doc_id: str = Field(description="ID of the document to edit"),
        old_str: str = Field(description="The text to replace. Must match exactly, including whitespace"),
        new_str: str = Field(description="New text to insert8 in the document content"),
):
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} does not exist")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


# Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_documents() -> list[str]:
    return list(docs.keys())


# Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def fetch_document(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id {doc_id} does not exist")
    return docs[doc_id]


# Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
        doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat the contents of the document in Markdown format. 

    The id of the document you need to format is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [
        base.UserMessage(prompt)
    ]


# Write a prompt to summarize a doc
@mcp.prompt(
    name="summarize",
    description="Summarizes the contents of the document."
)
def summarize_document(
        doc_id: str = Field(description="Id of the document to summarize")
) -> list[base.Message]:
    prompt = f"""
    Your goal is to summarize the contents of the ducument.

    The id of the ducument you need to summarize is:
    <ducument_id>
    {doc_id}
    </ducument_id>

    Keep the summary as brief as possible without missing any details. Give a clear and concise summary.
    """
    return [
        base.UserMessage(prompt)
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
