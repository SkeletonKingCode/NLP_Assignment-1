"use client";

import { useRef, useEffect } from "react";

export default function InputPanel({
    prefix,
    setPrefix,
    onSubmit,
    isLoading,
    clearError,
}) {
    const textareaRef = useRef(null);

    /* Auto-resize textarea up to 5 lines */
    useEffect(() => {
        const el = textareaRef.current;
        if (!el) return;
        el.style.height = "auto";
        const lineHeight = 28;
        const maxHeight = lineHeight * 5;
        el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`;
    }, [prefix]);

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSubmit();
        }
    };

    const handleChange = (e) => {
        setPrefix(e.target.value);
        if (clearError) clearError();
    };

    return (
        <div
            style={{
                padding: "1rem 1.25rem",
                borderTop: "1px solid #2a3a6e44",
                background: "#0d1225",
            }}
        >
            <div
                style={{
                    display: "flex",
                    alignItems: "flex-end",
                    gap: "0.75rem",
                    maxWidth: "800px",
                    margin: "0 auto",
                    background: "#1a2035",
                    borderRadius: "16px",
                    border: "1px solid #2a3a6e",
                    padding: "0.5rem 0.75rem",
                    transition: "border-color 0.3s",
                }}
            >
                {/* Submit button (left side in RTL = visually left) */}
                <button
                    onClick={onSubmit}
                    disabled={isLoading || !prefix.trim()}
                    style={{
                        width: "42px",
                        height: "42px",
                        minWidth: "42px",
                        borderRadius: "12px",
                        border: "none",
                        background:
                            isLoading || !prefix.trim() ? "#2a3a6e44" : "#4a6fa5",
                        color: isLoading || !prefix.trim() ? "#8892a4" : "#fff",
                        cursor:
                            isLoading || !prefix.trim() ? "not-allowed" : "pointer",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        transition: "all 0.2s",
                        flexShrink: 0,
                    }}
                    onMouseOver={(e) => {
                        if (!isLoading && prefix.trim())
                            e.currentTarget.style.background = "#6b8fc4";
                    }}
                    onMouseOut={(e) => {
                        if (!isLoading && prefix.trim())
                            e.currentTarget.style.background = "#4a6fa5";
                    }}
                >
                    {isLoading ? (
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            style={{ animation: "spin 1s linear infinite" }}
                        >
                            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
                            <circle
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                strokeWidth="3"
                                strokeDasharray="30 70"
                                strokeLinecap="round"
                            />
                        </svg>
                    ) : (
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="currentColor"
                        >
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                        </svg>
                    )}
                </button>

                {/* Textarea */}
                <textarea
                    ref={textareaRef}
                    value={prefix}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    placeholder="یہاں اپنی کہانی شروع کریں..."
                    rows={1}
                    disabled={isLoading}
                    className="urdu-text glow-border"
                    style={{
                        flex: 1,
                        background: "transparent",
                        border: "none",
                        outline: "none",
                        color: "#e8e8e8",
                        fontSize: "1.1rem",
                        lineHeight: "1.75",
                        resize: "none",
                        padding: "0.5rem 0",
                        boxShadow: "none",
                    }}
                />
            </div>
        </div>
    );
}
