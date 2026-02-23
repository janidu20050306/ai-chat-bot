import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def load_csv(path: Path):
    try:
        import pandas as pd
    except Exception:
        print("pandas not installed; skipping CSV load.")
        return []
    if not path.exists():
        return []
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        docs.append({
            "text": str(row.get("text", "")),
            "metadata": {"source": path.name},
        })
    return docs


def load_pdf(path: Path):
    if not path.exists():
        return []
    # Prefer langchain loader if available, otherwise fall back to pypdf
    try:
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(str(path))
        docs = loader.load()
        results = []
        for d in docs:
            text = getattr(d, "page_content", str(d))
            results.append({"text": text, "metadata": {"source": path.name}})
        return results
    except Exception:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            texts = []
            for p in reader.pages:
                texts.append(p.extract_text() or "")
            results = []
            for t in texts:
                results.append({"text": t, "metadata": {"source": path.name}})
            return results
        except Exception as e:
            print(f"Failed to load PDF {path}: {e}")
            return []


def main():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set. Set it in your shell or in .env")
    else:
        print(f"OPENAI_API_KEY found (length {len(key)})")

    base = Path(__file__).parent
    data_dir = base / "data"
    csv_docs = load_csv(data_dir / "data.csv")
    pdf_docs = load_pdf(data_dir / "sample.pdf")

    print(f"Loaded {len(csv_docs)} CSV docs and {len(pdf_docs)} PDF docs.")
    if csv_docs:
        print("First CSV doc:", csv_docs[0])
    if pdf_docs:
        print("First PDF doc:", pdf_docs[0])


if __name__ == "__main__":
    main()
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def load_csv(path: Path):
    try:
        import pandas as pd
    except Exception:
        print("pandas not installed; skipping CSV load.")
        return []
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return [{"text": str(row.get("text", "")), "metadata": {"source": path.name}} for _, row in df.iterrows()]


def load_pdf(path: Path):
    if not path.exists():
        return []
    # Prefer langchain loader if available, otherwise fall back to pypdf
    try:
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(str(path))
        docs = loader.load()
        return [{"text": getattr(d, "page_content", str(d)), "metadata": {"source": path.name}} for d in docs]
    except Exception:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            texts = [p.extract_text() or "" for p in reader.pages]
            return [{"text": t, "metadata": {"source": path.name}} for t in texts]
        except Exception as e:
            print(f"Failed to load PDF {path}: {e}")
            return []


def main():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set. Set it in your shell or in .env")
    else:
        print(f"OPENAI_API_KEY found (length {len(key)})")

    base = Path(__file__).parent
    data_dir = base / "data"
    csv_docs = load_csv(data_dir / "data.csv")
    pdf_docs = load_pdf(data_dir / "sample.pdf")

    print(f"Loaded {len(csv_docs)} CSV docs and {len(pdf_docs)} PDF docs.")
    if csv_docs:
        print("First CSV doc:", csv_docs[0])
    if pdf_docs:
        print("First PDF doc:", pdf_docs[0])


if __name__ == "__main__":
    main()
