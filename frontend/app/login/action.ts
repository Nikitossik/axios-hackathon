"use server";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export default async function UserLogin(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;
  const pararms = new URLSearchParams();
  pararms.append("email", email);
  pararms.append("password", password);
  try {
    const response = await fetch(
      `${process.env.FASTAPI_PUBLIC_API_URL}api/auth/token`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: pararms,
      },
    );
    if (!response.ok) {
      return { error: "Invalid email or password" };
    }
    const data = await response.json();
    const token = data.access_token;
    const cookieStore = await cookies();
    cookieStore.set("access_token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      path: "/",
    });
  } catch (error) {
    return { error: "An error occurred during login" };
  }
  redirect("/");
}
