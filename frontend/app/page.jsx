"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { generateStory, checkHealth } from "@/lib/api";
import StoryDisplay from "@/components/StoryDisplay";
import InputPanel from "@/components/InputPanel";
import SettingsPanel from "@/components/SettingsPanel";

export default function Home() {
    /* ─── state ─── */
    const [prefix, setPrefix] = useState("");
    const [story, setStory] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [tokensGenerated, setTokensGenerated] = useState(null);
    const [apiOnline, setApiOnline] = useState(null);
    const [settings, setSettings] = useState({
        maxLength: 500,
        temperature: 0.8,
        topK: 7,
    });
    const [displayedStory, setDisplayedStory] = useState("");
    const [isTypewriting, setIsTypewriting] = useState(false);

    const typewriterRef = useRef(null);
    const inputRef = useRef(null);

    /* ─── health check on mount ─── */
    useEffect(() => {
        checkHealth().then(setApiOnline);
    }, []);

    /* ─── auto-dismiss errors after 5 seconds ─── */
    useEffect(() => {
        if (!error) return;
        const t = setTimeout(() => setError(null), 5000);
        return () => clearTimeout(t);
    }, [error]);

    /* ─── typewriter effect (word-by-word) ─── */
    useEffect(() => {
        if (!story) return;

        // Cancel any running typewriter
        if (typewriterRef.current) clearInterval(typewriterRef.current);

        const words = story.split(/(\s+)/); // keep whitespace tokens
        let idx = 0;
        setDisplayedStory("");
        setIsTypewriting(true);

        typewriterRef.current = setInterval(() => {
            // Reveal 3-5 words per tick
            const chunk = words.slice(idx, idx + 4).join("");
            idx += 4;

            setDisplayedStory((prev) => prev + chunk);

            if (idx >= words.length) {
                clearInterval(typewriterRef.current);
                typewriterRef.current = null;
                setIsTypewriting(false);
            }
        }, 80);

        return () => {
            if (typewriterRef.current) {
                clearInterval(typewriterRef.current);
                typewriterRef.current = null;
            }
        };
    }, [story]);

    /* ─── submit handler ─── */
    const handleSubmit = useCallback(async () => {
        const trimmed = prefix.trim();
        if (!trimmed) return;

        // Client-side validation
        if (trimmed.length < 3) {
            setError("براہ کرم کم از کم ۳ حروف لکھیں");
            return;
        }

        setIsLoading(true);
        setError(null);
        setStory("");
        setDisplayedStory("");
        setTokensGenerated(null);

        // Cancel any running typewriter
        if (typewriterRef.current) {
            clearInterval(typewriterRef.current);
            typewriterRef.current = null;
        }

        try {
            const result = await generateStory({
                prefix: trimmed,
                maxLength: settings.maxLength,
                temperature: settings.temperature,
                topK: settings.topK,
            });
            setStory(result.story);
            setTokensGenerated(result.tokens_generated);
        } catch (err) {
            setError("کہانی بنانے میں مسئلہ آ گیا، دوبارہ کوشش کریں");
        } finally {
            setIsLoading(false);
        }
    }, [prefix, settings]);

    /* ─── new story handler ─── */
    const handleNewStory = () => {
        setStory("");
        setDisplayedStory("");
        setTokensGenerated(null);
        setError(null);
        setPrefix("");
        if (typewriterRef.current) {
            clearInterval(typewriterRef.current);
            typewriterRef.current = null;
        }
        setIsTypewriting(false);
    };

    /* ─── render ─── */
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                height: "100vh",
                overflow: "hidden",
            }}
        >
            {/* ═══════ HEADER ═══════ */}
            <header
                style={{
                    background: "#111827",
                    borderBottom: "1px solid #d4a84344",
                    padding: "0.75rem 1.5rem",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    flexShrink: 0,
                }}
            >
                <h1
                    className="urdu-text"
                    style={{
                        fontSize: "1.6rem",
                        color: "#d4a843",
                        margin: 0,
                        fontWeight: 700,
                        lineHeight: "1.4",
                    }}
                >
                    قصہ گو
                </h1>
                <span
                    className="urdu-text"
                    style={{
                        fontSize: "0.9rem",
                        color: "#8892a4",
                        lineHeight: "1.4",
                    }}
                >
                    اردو کہانیوں کا جادو
                </span>
            </header>

            {/* ═══════ API STATUS ═══════ */}
            {apiOnline !== null && (
                <div
                    style={{
                        padding: "0.4rem 1.5rem",
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        background: apiOnline ? "transparent" : "#f8717115",
                        justifyContent: "flex-start",
                    }}
                >
                    <span
                        style={{
                            width: "8px",
                            height: "8px",
                            borderRadius: "50%",
                            background: apiOnline ? "#34d399" : "#f87171",
                            display: "inline-block",
                            boxShadow: apiOnline
                                ? "0 0 6px #34d399"
                                : "0 0 6px #f87171",
                        }}
                    />
                    <span
                        className="urdu-text"
                        style={{
                            fontSize: "0.75rem",
                            color: apiOnline ? "#34d399" : "#f87171",
                            lineHeight: "1.4",
                        }}
                    >
                        {apiOnline
                            ? "سرور متصل ہے"
                            : "سرور سے رابطہ نہیں ہو سکا"}
                    </span>
                </div>
            )}

            {/* ═══════ STORY DISPLAY ═══════ */}
            <StoryDisplay
                displayedStory={displayedStory}
                fullStory={story}
                isTypewriting={isTypewriting}
                tokensGenerated={tokensGenerated}
                error={error}
                onNewStory={handleNewStory}
                inputRef={inputRef}
            />

            {/* ═══════ SETTINGS ═══════ */}
            <SettingsPanel
                settings={settings}
                onSettingsChange={setSettings}
            />

            {/* ═══════ INPUT ═══════ */}
            <InputPanel
                prefix={prefix}
                setPrefix={setPrefix}
                onSubmit={handleSubmit}
                isLoading={isLoading}
                clearError={() => setError(null)}
            />
        </div>
    );
}
