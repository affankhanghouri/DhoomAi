import type { Metadata } from "next"
import {
  Cormorant_Garamond,
  Noto_Nastaliq_Urdu,
  Outfit,
  Space_Grotesk,
} from "next/font/google"
import "./globals.css"

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-body",
})

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-heading",
})

const sageSerif = Cormorant_Garamond({
  subsets: ["latin"],
  variable: "--font-sage",
  weight: ["400", "500", "600", "700"],
})

const nastaliq = Noto_Nastaliq_Urdu({
  subsets: ["arabic"],
  variable: "--font-urdu",
  weight: ["400", "500", "600", "700"],
})

export const metadata: Metadata = {
  title: "Dhoom AI",
  description: "AI campaign operator for Pakistani sellers.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body
        className={`${outfit.variable} ${spaceGrotesk.variable} ${sageSerif.variable} ${nastaliq.variable}`}
      >
        {children}
      </body>
    </html>
  )
}