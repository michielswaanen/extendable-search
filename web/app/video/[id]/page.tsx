"use client"

import DetailHeader from "@/components/video/DetailHeader";
import { useParams } from 'next/navigation';

export default function SearchResultDetail() {

    // /////////////////////////////////// //
    //                                     //
    //                 Hooks               //
    //                                     //
    // /////////////////////////////////// //


    const {id} = useParams()


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
            </>
        )
    }

    return render();
}
