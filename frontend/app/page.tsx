import { serverFetch } from "./lib/api/server";
import { oswald } from "./ui/fonts";
import type { PaginatedUsers } from "./lib/type";
import Header from "@/app/widgets/Header";

export default async function Home() {
  const response = await serverFetch("/api/user");
  const data: PaginatedUsers = response;

  return (
    <>
      <Header />
      <div className={`${oswald.className} flex justify-center`}>
        Hello, {data.items[0]?.name}
      </div>
    </>
  );
}
