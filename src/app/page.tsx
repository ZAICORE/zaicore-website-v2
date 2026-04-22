import { Nav } from "@/components/layout/Nav";
import { Footer } from "@/components/layout/Footer";
import { Hero } from "@/components/home/Hero";
import { EngineeringSection } from "@/components/home/EngineeringSection";
import { SecuritySection } from "@/components/home/SecuritySection";

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <EngineeringSection />
        <SecuritySection />
      </main>
      <Footer />
    </>
  );
}
