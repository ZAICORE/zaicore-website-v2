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
  /** Overrides the givenName+familyName default — for compound surnames. */
  initials?: string;
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

  jaymesonvasilakosmcrae: {
    slug: "jaymesonvasilakosmcrae",
    name: "Jaymeson Vasilakos McRae",
    givenName: "Jaymeson",
    familyName: "Vasilakos McRae",
    initials: "JM",
    title: "Chief Revenue Officer",
    company: "ZAICORE",
    companyUrl: "https://zaicore.com",
    bio: "Driving growth and revenue strategy across ZAICORE's engineering and security work.",
    city: "Oakville, ON",
    email: "jaymeson@zaicore.com",
    phone: "+1 (905) 464-5920",
    linkedin: "https://ca.linkedin.com/in/jaymesonvm",
    website: "https://zaicore.com",
    // photo: "/p/jaymesonvasilakosmcrae.jpg",
  },
};
