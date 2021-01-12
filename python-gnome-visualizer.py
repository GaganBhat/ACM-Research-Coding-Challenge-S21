from dna_features_viewer import BiopythonTranslator, CircularGraphicRecord

color_map = {
    "rep_origin": "yellow",
    "CDS": "orange",
    "regulatory": "red",
    "misc_recomb": "darkblue",
    "misc_feature": "lightblue",
}

translator = BiopythonTranslator(
    features_filters=(lambda f: f.type not in ["gene", "source"],),
    features_properties=lambda f: {"color": color_map.get(f.type, "white")},
)

translator.max_line_length = 15
graphic_record = translator.translate_record(
    "Genome.gb", record_class=CircularGraphicRecord
)

graphic_record.labels_spacing = 15


ax, _ = graphic_record.plot(figure_width=8, figure_height=11)
ax.figure.savefig("ACM_Circular_Genome_Representation.png")
