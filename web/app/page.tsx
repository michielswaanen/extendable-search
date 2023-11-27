import Container from "@/components/Container";
import Header from "@/components/Header";
import SearchBox from "@/components/SearchBox";
import { SearchResults } from "@/components/SearchResults";

export default function Home() {
  return (
    <main className="flex w-full bg-white h-screen justify-center align">

      <Container>
        <Header />
        <div className="h-12" />
        <SearchBox />
        <div className="h-12" />
        <SearchResults />
      </Container>


    </main>
  )
}
