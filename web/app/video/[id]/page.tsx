"use client"

import DetailHeader from "@/components/video/DetailHeader";
import VideoSceneResults from "@/components/video/VideoSceneResults";
import { useMount } from "@/core/hooks/useMount";
import useScenes from "@/core/state/useScenes";
import useVideo from "@/core/state/useVideo";
import { useParams } from 'next/navigation';

export default function SearchResultDetail() {

    // /////////////////////////////////// //
    //                                     //
    //                 Hooks               //
    //                                     //
    // /////////////////////////////////// //


    const { id } = useParams();
    const { fetchScenes, scenes } = useScenes();
    const { fetchVideo, video } = useVideo();

    useMount(() => {
        fetchVideo(id as string);
        fetchScenes(id as string);
    })


    // /////////////////////////////////// //
    //                                     //
    //                 Render              //
    //                                     //
    // /////////////////////////////////// //

    const render = () => {
        const videoId = id as string || "unknown";

        return (
            <>
                <DetailHeader videoId={videoId} />
                <div className="h-12" />
                <VideoSceneResults video={video} scenes={scenes} />
            </>
        )
    }

    return render();
}
