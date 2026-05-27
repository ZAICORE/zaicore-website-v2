/**
 * Personal profile cards for ZAICORE folks.
 *
 * Each entry powers /p/[slug] (visible profile) and
 * /api/p/[slug]/vcard (Save-Contact download). Add a person by
 * appending here — no other file edits required.
 *
 * Photo: drop a square image at /public/p/<slug>.jpg (or .png).
 * If absent, the page renders initials in a lapis circle.
 */

export interface Person {
  slug: string;
  name: string;
  givenName: string;
  familyName: string;
  title: string;
  company: string;
  companyUrl?: string;
  bio: string;
  city?: string;
  email?: string;
  phone?: string;
  linkedin?: string;
  twitter?: string;
  github?: string;
  website?: string;
  photo?: string;
}

export const people: Record<string, Person> = {
  zacharyferguson: {
    slug: "zacharyferguson",
    name: "Zachary Ferguson",
    givenName: "Zachary",
    familyName: "Ferguson",
    title: "Founder & CEO",
    company: "ZAICORE",
    companyUrl: "https://zaicore.com",
    bio: "Building AI engineering and applied security from Oakville.",
    city: "Oakville, ON",
    email: "zachary@zaicore.com",
    phone: "+1 (905) 599-6864",
    linkedin: "https://www.linkedin.com/in/zacharyferguson/",
    website: "https://zaicore.com",
    // photo: "/p/zacharyferguson.jpg",   // drop a square image at /public/p/zacharyferguson.jpg to enable
  },
};
