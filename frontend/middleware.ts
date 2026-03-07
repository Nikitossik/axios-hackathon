import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

function decodeToken(token: string) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role;
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
}

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const currentPath = request.nextUrl.pathname;
  if (!token) {
    if (currentPath !== "/login") {
      return NextResponse.redirect(new URL("/login", request.url));
    }
    return NextResponse.next();
  }
  const role = decodeToken(token);
  if (role !== "admin" && currentPath.startsWith("/admin")) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  if (currentPath === "/" && role === "admin") {
    return NextResponse.redirect(new URL("/admin", request.url));
  }
  if (currentPath === "/login") {
    const redirectUrl = role === "admin" ? "/admin" : "/";
    return NextResponse.redirect(new URL(redirectUrl, request.url));
  }
  return NextResponse.next();
}
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
