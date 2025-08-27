import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

// Use system fonts to avoid Google Fonts connectivity issues
// If you need Inter font later, you can uncomment the import above
// import { Inter } from "next/font/google";
// const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Smart Office - سیستم مدیریت خدمات",
  description: "سیستم جامع مدیریت خدمات چاپ، تایپ و فروشگاه دیجیتال",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl">
      <body className="font-sans">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
