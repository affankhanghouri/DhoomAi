import { Header } from "@/components/landing/header"
import { HeroSection } from "@/components/landing/hero-section"
import { CreativeAdvantageSection } from "@/components/landing/creative-advantage-section"
import { CampaignTransformSection } from "@/components/landing/campaign-transform-section"
import { CampaignGallerySection } from "@/components/landing/campaign-gallery-section"
import { RevealTextSection } from "@/components/landing/reveal-text-section"
import { OutputSection } from "@/components/landing/output-section"
import { FinalCtaSection } from "@/components/landing/final-cta-section"
import { CreativeLabShowcaseSection } from "@/components/landing/creative-lab-showcase-section"
export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      <Header />
      <HeroSection />
    

<section
  id="problem"
  className="relative overflow-hidden bg-[#fbf7ff] px-5 py-14 md:px-10 md:py-16"
>
  <div className="mx-auto max-w-[860px] text-center">
   

    <h2 className="mx-auto max-w-[760px] text-[clamp(2rem,3.6vw,3.8rem)] font-black leading-[0.98] tracking-[-0.075em] text-[#070816]">
      Most sellers do not lose because their product is bad.
    </h2>

    <p className="mx-auto mt-5 max-w-[680px] text-[clamp(1rem,1.6vw,1.45rem)] font-bold leading-[1.35] tracking-[-0.035em] text-slate-600">
      They lose because the product has no clear marketing strategy.
    </p>
  </div>
</section>

      <CampaignTransformSection />
<CreativeLabShowcaseSection />
      <CampaignGallerySection />
   
<RevealTextSection />
<FinalCtaSection />
    </main>
  )
}