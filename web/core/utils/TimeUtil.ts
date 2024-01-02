class TimeUtil {

    public static beautify(seconds: number) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.round(seconds % 60);
        return `${minutes}m ${remainingSeconds}s`;
    }

}

export default TimeUtil;