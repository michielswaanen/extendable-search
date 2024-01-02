import { Scene } from "@/core/state/useScenes"
import { Video } from "@/core/state/useVideos"
import TimeUtil from "@/core/utils/TimeUtil"

type Props = {
    video: Video | undefined,
    scenes: Scene[] | undefined
}

export default function VideoSceneResults(props: Props) {

    // /////////////////////////////////// //
    //                                     //
    //                 Render              //
    //                                     //
    // /////////////////////////////////// //

    const renderScenes = (video: Video, scenes: Scene[]) => {
        const SceneList = scenes.map((scene, index) => {
            const start = TimeUtil.beautify(scene.start / Number(video.fps))
            const end = TimeUtil.beautify(scene.end / Number(video.fps))

            return (
                <div key={index} className="flex flex-row w-full gap-4 items-center p-4 bg-white rounded-lg shadow-lg">
                    <p className="flex h-12 w-12 bg-gray-200 rounded-lg items-center justify-center text-">{index}</p>
                    <p className="text-gray-600">{start} - {end}</p>
                </div>
            )
        });

        return (
            <div className="grid grid-cols-3 gap-4">
                {SceneList}
            </div>
        )
    }

    const render = () => {
        if (!props.video || !props.scenes) {
            return <div>Loading...</div>
        }

        return renderScenes(props.video, props.scenes);
    }

    return render();
}