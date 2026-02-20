import "./globals.css";

export const metadata = {
    title: "قصہ گو - Urdu Story Generator",
    description:
        "اردو کہانیوں کا جادوئی نظام — Urdu Children's Story Generation powered by a Trigram Language Model",
};

export default function RootLayout({ children }) {
    return (
        <html lang="ur">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link
                    rel="preconnect"
                    href="https://fonts.gstatic.com"
                    crossOrigin="anonymous"
                />
                <link
                    href="https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap"
                    rel="stylesheet"
                />
            </head>
            <body
                dir="rtl"
                style={{
                    backgroundColor: "#0a0f1e",
                    color: "#e8e8e8",
                    fontFamily:
                        "'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif",
                    margin: 0,
                    minHeight: "100vh",
                }}
            >
                {children}
            </body>
        </html>
    );
}
