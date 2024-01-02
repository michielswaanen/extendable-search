import { EarIcon, EyeIcon, ScanFaceIcon, SearchIcon, SpeechIcon } from "lucide-react";
import { ReactElement } from "react";

export default function SearchBox() {

    const renderLabel = (icon: ReactElement, text: string) => {
        return <div className="flex flex-row items-center gap-1.5 bg-white px-3 py-2 rounded-xl border shadow-sm cursor-pointer hover:bg-gray-50">
            {icon}
            <p>{text}</p>
        </div>
    }

    return <div className="flex flex-col w-full">
        <div className="relative w-full">
            {/* Icon */}
            <div className="absolute w-12 h-full flex items-center justify-center">
                <SearchIcon size={20} className="relative text-slate-400" />
            </div>

            {/* Input */}
            <input type="text" className="w-full pl-12 pr-24 py-4 rounded-xl border shadow-sm" placeholder="Start searching..." />
        </div>
        <div className="flex flex-row gap-2 mt-2">
            {renderLabel(<EarIcon size={20} className="relative text-slate-400" />, "Sound")}
            {renderLabel(<EyeIcon size={20} className="relative text-slate-400" />, "Vision")}
            {renderLabel(<ScanFaceIcon size={20} className="relative text-slate-400" />, "Person")}

        </div>
    </div>
}