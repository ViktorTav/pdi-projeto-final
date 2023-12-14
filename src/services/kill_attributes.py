class KillAttributes:
    attributes = {
        3:{
            "name": "shot_through_wall"
        },
        8:{
            "name": "headshot"
        }
    }

    @staticmethod
    def get_kill_attributes_from_stats(stats):
        attributes = []

        for stat in stats:
            if len(stat) in KillAttributes.attributes:
                attributes.append(KillAttributes.attributes[len(stat)])

        return attributes