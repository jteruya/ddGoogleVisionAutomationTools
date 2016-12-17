DROP TABLE IF EXISTS JT.Compute_Vision_Hackday;
CREATE TABLE JT.Compute_Vision_Hackday (
        ApplicationId TEXT,
        Created TIMESTAMP,
        ImageFileName TEXT,
        FaceAnnotations JSONB,
        LabelAnnotations JSONB,
        SafeSearchAnnotation JSONB,
        TextAnnotations JSONB,
        LandmarkAnnotations JSONB,
        LogoAnnotations JSONB
);
