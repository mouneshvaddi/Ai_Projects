
import { useEffect } from "react";
import {
  ArrowUpRight, BookOpen, BrainCircuit,
  CalendarDays, Globe2, Sparkles, X
} from "lucide-react";
import "./ArticleReader.css";

function parseBriefing(text = "") {
  const normalized = text.replace(/\\n/g, "\n");

  const getSection = (name, nextNames = []) => {
    const escaped = nextNames.join("|");
    const pattern = new RegExp(
      `${name}\\s*:\\s*([\\s\\S]*?)(?=${escaped ? `(?:${escaped})\\s*:` : "$"})`,
      "i"
    );
    return normalized.match(pattern)?.[1]?.trim() || "";
  };

  return {
    summary: getSection("SUMMARY", [
      "KEY TAKEAWAYS", "CATEGORY", "WHY IT MATTERS"
    ]),
    takeaways: getSection("KEY TAKEAWAYS", [
      "CATEGORY", "WHY IT MATTERS"
    ]),
    impact: getSection("WHY IT MATTERS")
  };
}

export default function ArticleReader({ article, onClose }) {
  useEffect(() => {
    if (!article) return;

    const handleEscape = (event) => {
      if (event.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleEscape);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = previousOverflow;
    };
  }, [article, onClose]);

  if (!article) return null;

  const briefing = parseBriefing(article.summary_text || "");
  const takeaways = briefing.takeaways
    .split(/\n|(?=\d+\.\s)/)
    .map((item) => item.replace(/^\d+\.\s*/, "").trim())
    .filter(Boolean);

  return (
    <div className="reader-overlay" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose();
    }}>
      <div className="reader-panel" role="dialog" aria-modal="true"
        aria-label="Article intelligence briefing">

        <div className="reader-toolbar">
          <div className="reader-brand">
            <BrainCircuit size={19} />
            NEWSGEN <span>/ INTELLIGENCE BRIEFING</span>
          </div>
          <button className="reader-close" onClick={onClose}
            aria-label="Close article">
            <X size={20} />
          </button>
        </div>

        <div className="reader-content">
          <div className="reader-eyebrow">
            <Sparkles size={15} /> AI-DECODED INTELLIGENCE
          </div>

          <div className="reader-category">
            {article.category || "GENERAL INTELLIGENCE"}
          </div>

          <h1>{article.headline || article.title}</h1>

          <div className="reader-meta">
            <span><Globe2 size={15} /> {article.source || "News source"}</span>
            <span><CalendarDays size={15} /> {article.published || "Date unavailable"}</span>
          </div>

          <div className="reader-divider" />

          <section className="reader-section">
            <div className="reader-section-label">
              <BookOpen size={16} /> THE INTELLIGENCE BRIEF
            </div>
            <p>
              {briefing.summary ||
                article.description ||
                "No summary available for this article."}
            </p>
          </section>

          {takeaways.length > 0 && (
            <section className="reader-section">
              <div className="reader-section-label">
                <Sparkles size={16} /> KEY TAKEAWAYS
              </div>
              <div className="reader-takeaways">
                {takeaways.map((point, index) => (
                  <div className="reader-takeaway" key={index}>
                    <span>{String(index + 1).padStart(2, "0")}</span>
                    <p>{point}</p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {briefing.impact && (
            <section className="reader-impact">
              <span>WHY THIS STORY MATTERS</span>
              <p>{briefing.impact}</p>
            </section>
          )}

          <div className="reader-actions">
            {article.url ? (
              <a href={article.url} target="_blank"
                rel="noopener noreferrer">
                EXPLORE ORIGINAL SOURCE <ArrowUpRight size={17} />
              </a>
            ) : (
              <span>Original source URL unavailable</span>
            )}
          </div>

          <p className="reader-disclaimer">
            AI-generated interpretation based on collected news content.
            Verify important details using the original source.
          </p>
        </div>
      </div>
    </div>
  );
}
