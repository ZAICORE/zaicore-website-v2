/**
 * vCard download for a Person card. Powers the "Save Contact"
 * button on /p/[slug] — opens iOS / Android contacts directly.
 */

import { NextResponse } from "next/server";
import { people } from "@/content/people";

interface Params {
  params: Promise<{ slug: string }>;
}

function esc(s: string): string {
  // RFC 6350 escaping for TEXT values
  return s.replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/,/g, "\\,").replace(/;/g, "\\;");
}

export async function GET(_req: Request, { params }: Params) {
  const { slug } = await params;
  const p = people[slug];
  if (!p) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  const lines: string[] = [];
  lines.push("BEGIN:VCARD");
  lines.push("VERSION:3.0");
  lines.push(`N:${esc(p.familyName)};${esc(p.givenName)};;;`);
  lines.push(`FN:${esc(p.name)}`);
  lines.push(`ORG:${esc(p.company)}`);
  lines.push(`TITLE:${esc(p.title)}`);
  if (p.email) lines.push(`EMAIL;TYPE=INTERNET:${p.email}`);
  if (p.phone) lines.push(`TEL;TYPE=CELL:${p.phone}`);
  if (p.linkedin) lines.push(`URL;TYPE=LinkedIn:${p.linkedin}`);
  if (p.twitter) lines.push(`URL;TYPE=Twitter:${p.twitter}`);
  if (p.github) lines.push(`URL;TYPE=GitHub:${p.github}`);
  if (p.website) lines.push(`URL;TYPE=Website:${p.website}`);
  if (p.companyUrl && p.companyUrl !== p.website) lines.push(`URL;TYPE=Company:${p.companyUrl}`);
  if (p.city) lines.push(`ADR;TYPE=WORK:;;;${esc(p.city)};;;`);
  if (p.bio) lines.push(`NOTE:${esc(p.bio)}`);
  lines.push("END:VCARD");

  // Use CRLF per RFC 6350.
  const body = lines.join("\r\n") + "\r\n";

  return new NextResponse(body, {
    status: 200,
    headers: {
      "Content-Type": "text/vcard; charset=utf-8",
      "Content-Disposition": `attachment; filename="${p.slug}.vcf"`,
      "Cache-Control": "public, max-age=300",
    },
  });
}
