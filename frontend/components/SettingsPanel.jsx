"use client";

import { useState } from "react";

export default function SettingsPanel({ settings, onSettingsChange }) {
    const [isOpen, setIsOpen] = useState(false);

    const update = (key, value) => {
        onSettingsChange({ ...settings, [key]: value });
    };

    return (
        <div style={{ borderTop: "1px solid #2a3a6e22" }}>
            {/* Toggle button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="urdu-text w-full py-2.5 px-4 flex items-center justify-between transition-colors duration-200"
                style={{
                    background: "transparent",
                    border: "none",
                    color: "#8892a4",
                    cursor: "pointer",
                    fontSize: "0.95rem",
                }}
            >
                <span>{isOpen ? "ترتیبات ▲" : "ترتیبات ▼"}</span>
            </button>

            {/* Collapsible panel */}
            <div
                className={`settings-panel ${isOpen ? "open" : ""}`}
                style={{ padding: isOpen ? "0 1.5rem 1.25rem" : "0 1.5rem" }}
            >
                <div className="flex flex-col gap-6">
                    {/* Story Length */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <span className="urdu-text" style={{ color: "#e8e8e8", fontSize: "0.95rem", lineHeight: "1.4" }}>
                                کہانی کی لمبائی
                            </span>
                            <span
                                style={{
                                    color: "#4a6fa5",
                                    fontFamily: "system-ui, sans-serif",
                                    fontSize: "0.85rem",
                                    direction: "ltr",
                                }}
                            >
                                {settings.maxLength}
                            </span>
                        </div>
                        <input
                            type="range"
                            min={50}
                            max={2000}
                            step={50}
                            value={settings.maxLength}
                            onChange={(e) => update("maxLength", Number(e.target.value))}
                        />
                        <p className="urdu-text mt-1" style={{ color: "#8892a4", fontSize: "0.75rem", lineHeight: "1.6" }}>
                            کہانی میں زیادہ سے زیادہ الفاظ کی تعداد
                        </p>
                    </div>

                    {/* Temperature */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <span className="urdu-text" style={{ color: "#e8e8e8", fontSize: "0.95rem", lineHeight: "1.4" }}>
                                تخلیقیت
                            </span>
                            <span
                                style={{
                                    color: "#4a6fa5",
                                    fontFamily: "system-ui, sans-serif",
                                    fontSize: "0.85rem",
                                    direction: "ltr",
                                }}
                            >
                                {settings.temperature.toFixed(1)}
                            </span>
                        </div>
                        <input
                            type="range"
                            min={0.1}
                            max={2.0}
                            step={0.1}
                            value={settings.temperature}
                            onChange={(e) => update("temperature", Number(e.target.value))}
                        />
                        <p className="urdu-text mt-1" style={{ color: "#8892a4", fontSize: "0.75rem", lineHeight: "1.6" }}>
                            زیادہ قدر = زیادہ تخلیقی، کم قدر = زیادہ محفوظ
                        </p>
                    </div>

                    {/* Top-K */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <span className="urdu-text" style={{ color: "#e8e8e8", fontSize: "0.95rem", lineHeight: "1.4" }}>
                                الفاظ کا انتخاب
                            </span>
                            <span
                                style={{
                                    color: "#4a6fa5",
                                    fontFamily: "system-ui, sans-serif",
                                    fontSize: "0.85rem",
                                    direction: "ltr",
                                }}
                            >
                                {settings.topK}
                            </span>
                        </div>
                        <input
                            type="range"
                            min={1}
                            max={50}
                            step={1}
                            value={settings.topK}
                            onChange={(e) => update("topK", Number(e.target.value))}
                        />
                        <p className="urdu-text mt-1" style={{ color: "#8892a4", fontSize: "0.75rem", lineHeight: "1.6" }}>
                            ہر مرحلے پر کتنے ممکنہ الفاظ میں سے انتخاب ہو
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
