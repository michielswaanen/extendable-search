import { useState } from "react"

export type Scene = {
    id: string
    start: number
    end: number
}

const useScenes = () => {

    const [scenes, setScenes] = useState<Scene[]>([])

    const fetchScenes = async (videoId: string) => {
        const url = `http://localhost:3001/videos/${videoId}/scenes`
        const scenes = await (await fetch(url)).json();

        for (const scene of scenes) {
            setScenes((prev) => [...prev, {
                id: scene[0],
                start: scene[2],
                end: scene[3]
            }])
        }
    }

    return {
        scenes,
        fetchScenes
    }
}

export default useScenes