"use client";

import { useRef, useEffect, useState } from "react";
import TypingIndicator from "./TypingIndicator";

export default function StoryDisplay({
    displayedStory,
    fullStory,
    isTypewriting,
    tokensGenerated,
    error,
    onNewStory,
    inputRef,
}) {
    const scrollRef = useRef(null);
    const [copied, setCopied] = useState(false);

    /* Auto-scroll to bottom as text appears */
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [displayedStory]);

    /* Copy story to clipboard */
    const handleCopy = async () => {
        if (!fullStory) return;
        try {
            await navigator.clipboard.writeText(fullStory);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch {
            /* fallback */
        }
    };

    /* New story */
    const handleNewStory = () => {
        setCopied(false);
        onNewStory();
    };

    /* Count Urdu words */
    const wordCount = fullStory
        ? fullStory
            .split(/\s+/)
            .filter((w) => w.length > 0).length
        : 0;

    const isComplete = fullStory && !isTypewriting;
    const isEmpty = !displayedStory && !error;

    return (
        <div
            ref={scrollRef}
            style={{
                flex: 1,
                overflowY: "auto",
                padding: "2rem 1.25rem",
                display: "flex",
                flexDirection: "column",
            }}
        >
            <div style={{ maxWidth: "800px", margin: "0 auto", width: "100%" }}>
                {/* Error state */}
                {error && (
                    <div
                        className="fade-in"
                        style={{
                            background: "#f8717122",
                            border: "1px solid #f8717144",
                            borderRadius: "12px",
                            padding: "1.25rem",
                            marginBottom: "1rem",
                        }}
                    >
                        <p
                            className="urdu-text"
                            style={{ color: "#f87171", fontSize: "1rem", margin: 0, lineHeight: "1.8" }}
                        >
                            {error}
                        </p>
                    </div>
                )}

                {/* Empty / welcome state */}
                {isEmpty && (
                    <div
                        className="fade-in"
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                            minHeight: "50vh",
                            textAlign: "center",
                            gap: "1.5rem",
                        }}
                    >
                        {/* Decorative character */}
                        <span
                            style={{
                                fontSize: "5rem",
                                color: "#d4a843",
                                opacity: 0.3,
                                lineHeight: 1,
                                fontFamily: "'Noto Nastaliq Urdu', serif",
                            }}
                        >
                            ب
                        </span>
                        <h2
                            className="urdu-text"
                            style={{
                                fontSize: "1.6rem",
                                color: "#e8e8e8",
                                margin: 0,
                                textAlign: "center",
                            }}
                        >
                            اپنی کہانی کا آغاز کریں
                        </h2>
                        <p
                            className="urdu-text"
                            style={{
                                fontSize: "1rem",
                                color: "#8892a4",
                                margin: 0,
                                maxWidth: "400px",
                                textAlign: "center",
                                lineHeight: "2",
                            }}
                        >
                            نیچے اپنا پہلا جملہ لکھیں اور کہانی خود بن جائے گی
                        </p>
                    </div>
                )}

                {/* Story text */}
                {displayedStory && (
                    <div className="fade-in">
                        <p
                            className={`urdu-text ${isTypewriting ? "typewriter-cursor" : ""}`}
                            style={{
                                fontSize: "1.3rem",
                                color: "#f0e6d3",
                                lineHeight: "2.2",
                                margin: 0,
                                whiteSpace: "pre-wrap",
                            }}
                        >
                            {displayedStory}
                        </p>

                        {/* Typing indicator */}
                        <TypingIndicator visible={isTypewriting} />

                        {/* Completion bar */}
                        {isComplete && (
                            <div
                                className="fade-in"
                                style={{
                                    marginTop: "2rem",
                                    paddingTop: "1.25rem",
                                    borderTop: "1px solid #2a3a6e44",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "space-between",
                                    flexWrap: "wrap",
                                    gap: "1rem",
                                }}
                            >
                                {/* Stats */}
                                <div
                                    className="urdu-text"
                                    style={{
                                        fontSize: "0.85rem",
                                        color: "#8892a4",
                                        lineHeight: "1.4",
                                    }}
                                >
                                    الفاظ: {wordCount} | ٹوکن: {tokensGenerated}
                                </div>

                                {/* Action buttons */}
                                <div style={{ display: "flex", gap: "0.75rem" }}>
                                    <button
                                        onClick={handleCopy}
                                        style={{
                                            background: copied ? "#34d39922" : "#1a2035",
                                            border: `1px solid ${copied ? "#34d399" : "#2a3a6e"}`,
                                            borderRadius: "10px",
                                            padding: "0.5rem 1rem",
                                            color: copied ? "#34d399" : "#8892a4",
                                            cursor: "pointer",
                                            fontFamily:
                                                "'Noto Nastaliq Urdu', serif",
                                            fontSize: "0.85rem",
                                            transition: "all 0.2s",
                                        }}
                                    >
                                        {copied ? "کاپی ہو گیا ✓" : "کاپی کریں"}
                                    </button>
                                    <button
                                        onClick={handleNewStory}
                                        style={{
                                            background: "#4a6fa522",
                                            border: "1px solid #4a6fa544",
                                            borderRadius: "10px",
                                            padding: "0.5rem 1rem",
                                            color: "#4a6fa5",
                                            cursor: "pointer",
                                            fontFamily:
                                                "'Noto Nastaliq Urdu', serif",
                                            fontSize: "0.85rem",
                                            transition: "all 0.2s",
                                        }}
                                    >
                                        نئی کہانی
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
