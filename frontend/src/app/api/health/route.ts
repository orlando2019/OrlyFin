import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "ok",
    service: "orlyfin-frontend",
    version: "v1",
    timestamp: new Date().toISOString(),
  });
}
