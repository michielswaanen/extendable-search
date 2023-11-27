import { useState } from "react"

type SearchMode = 'sound' | 'vision' | 'person'

export const useSearch = () => {

    const [query, setQuery] = useState('')
    const [mode, setMode] = useState<SearchMode>('sound')

    const submit = () => {

    }

    return {
        query,
        setQuery,
        mode,
        setMode,
        submit
    }
}