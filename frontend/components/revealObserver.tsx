"use client"

import { useEffect } from "react"

export default function RevealObserver() {
  useEffect(() => {
    const els = document.querySelectorAll(".dhoom-reveal")
    const observer = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("is-visible")
          observer.unobserve(e.target)
        }
      }),
      { threshold: 0.12 }
    )
    els.forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [])

  return null
}