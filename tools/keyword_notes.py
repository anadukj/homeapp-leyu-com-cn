from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a note associated with a keyword and a source URL."""
    keyword: str
    note: str
    source_url: str
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def formatted(self, separator: str = " | ") -> str:
        """Return a single-line string representation."""
        parts = [
            f"Keyword: {self.keyword}",
            f"Note: {self.note[:50]}{'...' if len(self.note) > 50 else ''}",
            f"Source: {self.source_url}",
            f"Created: {self.created_at}"
        ]
        return separator.join(parts)

    def brief(self) -> str:
        """Return a short summary line."""
        return f"[{self.keyword}] {self.note[:40]} — {self.source_url}"


@dataclass
class KeywordCollection:
    """A collection of KeywordNote instances with utility methods."""
    notes: List[KeywordNote] = field(default_factory=list)
    title: str = "Keyword Notes Collection"

    def add_note(self, keyword: str, note: str, source_url: str) -> None:
        """Add a new KeywordNote to the collection."""
        self.notes.append(KeywordNote(keyword=keyword, note=note, source_url=source_url))

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return all notes matching the given keyword (case-insensitive)."""
        return [n for n in self.notes if n.keyword.lower() == keyword.lower()]

    def find_by_url(self, url_fragment: str) -> List[KeywordNote]:
        """Return notes whose source_url contains the given fragment."""
        return [n for n in self.notes if url_fragment.lower() in n.source_url.lower()]

    def list_all(self) -> str:
        """Return a formatted multi-line string of all notes."""
        if not self.notes:
            return f"Collection '{self.title}' is empty."
        lines = [f"--- {self.title} ---"]
        for idx, note in enumerate(self.notes, 1):
            lines.append(f"{idx}. {note.formatted()}")
        return "\n".join(lines)

    def report_by_keyword(self) -> str:
        """Return a summary grouped by keyword."""
        groups: dict = {}
        for note in self.notes:
            groups.setdefault(note.keyword, []).append(note)
        lines = [f"Report: {self.title}"]
        for kw, items in groups.items():
            lines.append(f"\nKeyword '{kw}': {len(items)} note(s)")
            for item in items:
                lines.append(f"  - {item.brief()}")
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    collection = KeywordCollection(title="Demo Notes")

    # Add sample notes with the required keyword and URL
    collection.add_note(
        keyword="乐鱼体育",
        note="Official platform for sports and entertainment content.",
        source_url="https://homeapp-leyu.com.cn"
    )
    collection.add_note(
        keyword="乐鱼体育",
        note="Provides live streaming and interactive features.",
        source_url="https://homeapp-leyu.com.cn/about"
    )
    collection.add_note(
        keyword="python",
        note="A versatile programming language used for data analysis.",
        source_url="https://example.com/python-intro"
    )

    # Demonstrate output
    print(collection.list_all())
    print("\n" + "=" * 50)
    print(collection.report_by_keyword())
    print("\n" + "=" * 50)
    print("Search for '乐鱼体育':")
    for note in collection.find_by_keyword("乐鱼体育"):
        print(note.formatted())
    print("\nSearch for URL containing 'homeapp':")
    for note in collection.find_by_url("homeapp"):
        print(note.formatted())