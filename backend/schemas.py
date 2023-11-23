from marshmallow import Schema, fields

class DurationSchema(Schema):
    w_id = fields.Integer()
    video_id = fields.Integer()
    subtitle = fields.String()
    word = fields.String()
    video_duration_sec = fields.Float()
    duration_sec = fields.Float()
    word_speed = fields.String()
    character_count = fields.Integer()
    word_length = fields.String()
    vowel = fields.String()
    part_of_speech = fields.String()

class LinguisticTypeSchema(Schema):
    l_id = fields.Integer()
    video_id = fields.Integer()
    word = fields.String()
    subtitle = fields.String()
    video_duration_sec = fields.Float()
    duration_sec = fields.Float()
    phonemes = fields.String()
    visemes = fields.String()
    homophones = fields.String()
    HH = fields.String()

class NegativeWordsSchema(Schema):
    nw_id = fields.Integer()
    video_id = fields.Integer()
    word = fields.String()
    subtitle = fields.String()
    video_duration_sec = fields.Float()
    duration_sec= fields.Float()

class VideoClipsSchema(Schema):
    video_id = fields.Integer()
    subtitle = fields.String()
    video_duration_sec = fields.Float()
    word_count = fields.Integer()
    char_count = fields.Integer()
    video_length = fields.String()

    duration = fields.Nested(DurationSchema, many=True)
    linguistic_types = fields.Nested(LinguisticTypeSchema, many=True)
    negative_words = fields.Nested(NegativeWordsSchema, many=True)


class HomophonesSchema(Schema):
    HH = fields.String()
    record_count = fields.Integer()

class VideoClipsResultSchema(Schema):
    video_length = fields.String()
    record_count = fields.Integer()

class DurationResultSchema(Schema):
    part_of_speech = fields.String()
    record_count = fields.Integer()

class DurationSpeedResultSchema(Schema):
    word_speed = fields.String()
    record_count = fields.Integer()


class DurationLengthResultSchema(Schema):
    word_length = fields.String()
    record_count = fields.Integer()

class NegativeSchema(Schema):
    word= fields.String()
    record_count = fields.Integer()

class DurationWordResultSchema(Schema):
    word= fields.String()
    record_count = fields.Integer()