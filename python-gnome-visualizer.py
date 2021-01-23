from dna_features_viewer import BiopythonTranslator, CircularGraphicRecord
from Bio import Entrez, SeqIO
import moviepy.editor as mpe
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt


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


ax, _ = graphic_record.plot(figure_width=6, figure_height=6)
ax.figure.savefig("ACM_Circular_Genome_Representation.png")

duration = 5


def make_frame(t):
    top_nucleotide_index = t * graphic_record.sequence_length / duration
    graphic_record.top_position = top_nucleotide_index
    ax, _ = graphic_record.plot(figure_width=8, figure_height=11)
    ax.set_ylim(top=2)
    np_image = mplfig_to_npimage(ax.figure)
    plt.close(ax.figure)
    return np_image

clip = mpe.VideoClip(make_frame, duration=duration)
small_clip = clip.crop(x1=60, x2=-60, y1=100, y2=-100).resize(0.5)
small_clip.write_gif("circular_animation.gif", fps=60)