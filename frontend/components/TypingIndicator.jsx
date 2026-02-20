"use client";

export default function TypingIndicator({ visible }) {
    if (!visible) return null;

    return (
        <div className="fade-in flex items-center gap-3 py-3 px-4">
            <div className="flex items-center gap-1.5">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
            </div>
            <span
                className="urdu-text"
                style={{ fontSize: "0.9rem", color: "#8892a4", lineHeight: "1.4" }}
            >
                کہانی لکھی جا رہی ہے...
            </span>
        </div>
    );
}
