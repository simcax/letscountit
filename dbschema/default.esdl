module default {
    type counter{
        required uuid: uuid {
            constraint exclusive;
        };
        required name: str;
        count: int64 {
            default := 0
        }
    }
}
