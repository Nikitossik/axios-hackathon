import { oswald } from "../ui/fonts";
export default function Header() {
  return (
    <header className="bg-gray-800 text-white p-4">
      <h1 className={` ${oswald.className} text-xl font-bold`}>
        Axios Hackathon
      </h1>
    </header>
  );
}
