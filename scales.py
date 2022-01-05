import pandas as pd

from bokeh.plotting import figure, show
from bokeh.models import Label

import collections

notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
intervals_flats = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7']
intervals_sharps = ['1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7']
zipped_intervals = list(zip(intervals_flats, intervals_sharps))

root = 'A'
root_ix = notes.index(root)
rooted_notes = notes[root_ix:] + notes[:root_ix]
note_interval_map = {n: i for n, i in zip(rooted_notes, zipped_intervals)}
note_interval_map

class Fretboard:

    num_frets = 24
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    intervals_flats = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7'] * 2
    intervals_sharps = ['1', '#1', '2', '#2', '3', '4', '#4', '5', '#5', '6', '#6', '7'] * 2
    zipped_intervals = list(zip(intervals_flats, intervals_sharps))

    # String generator
    def generate_string(self, note):

        repeat_notes = self.notes * 4

        start_index = repeat_notes.index(note)
        end_index = start_index + self.num_frets

        return repeat_notes[start_index: end_index]

    # Convert output to DataFrames
    def convert_to_df(self):

        indices = ['LOW E', 'A', 'D', 'G', 'B', 'HI E']

        self.string_notes_df = pd.DataFrame(data=self.string_notes, index=indices)
        self.string_intervals_df = pd.DataFrame(data=self.string_intervals, index=indices)

    # On Instantiation
    def __init__(self, root, tuning=list('EADGBE')):

        self.tuning = tuning

        if root in self.notes:
            self.string_notes = [self.generate_string(s) for s in self.tuning]
            
            self.root = root
            root_ix = notes.index(root)
            rooted_notes = (self.notes[root_ix:] + self.notes[:root_ix]) * 2
            self.note_interval_map = {n: i for n, i in zip(rooted_notes, zipped_intervals)}        

            string_intervals = []
            for sn in self.string_notes:
                string_intervals.append([self.note_interval_map[n] for n in sn])

            self.string_intervals = string_intervals
            
            self.convert_to_df()

        else:
            Exception('Please enter a valid note as the root.')
    
class ScaleFinder:

    scale_map = {
            # Whole Fretboard
            'Whole Fretboard': ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7'],
            # Major Scale Modes
            'Major/Ionian': list('1234567'),
            'Dorian': ['1', '2', 'b3', '4', '5', '6', 'b7'],
            'Phrygian': ['1', 'b2', 'b3', '4', '5', 'b6', 'b7'],
            'Lydian': ['1', '2', '3', '#4', '5', '6', '7'],
            'Mixolydian': ['1', '2', '3', '4', '5', '6', 'b7'],
            'Minor/Aeolian': ['1', '2', 'b3', '4', '5', 'b6', 'b7'],
            'Locrian': ['1', 'b2', 'b3', '4', 'b5', 'b6', 'b7'],
            # Melodic Minor Scale Modes
            'Melodic Minor': ['1', '2', 'b3', '4', '5', '6', '7'],
            'Lydian Dominant': ['1', '2', '3', '#4', '5', '6', 'b7'],
            # Harmonic Minor Scale Modes
            'Harmonic Minor': ['1', '2', 'b3', '4', '5', 'b6', '7'],
            'Phrygian Dominant': ['1', 'b2', '3', '4', '5', 'b6', 'b7'],
            # Pentatonic Scales
            'Major Pentatonic': ['1', '2', '3', '5', '6'],
            'Minor Pentatonic': ['1', 'b3', '4', '5', 'b7'],
            'Dominant Pentatonic': ['1', '2', '3', '5', 'b7'],
            # Other Scales
            'Blues': ['1', 'b3', '4', 'b5', '5', 'b7'],
    }

    appregio_map = {
        'Major Triad': ['1', '3', '5'],
        'Minor Triad': ['1', 'b3', '5'],
        # 'Diminished Triad': [['1', 'b3', 'b5']],
        # 'Augmented Triad': [['1', '3', '#5']],
        'maj7': ['1', '3', '5', '7'],
        '7': ['1', '3', '5', 'b7'],
        'm7': ['1', 'b3', '5', 'b7'],
        'm7b5': ['1', 'b3', 'b5', 'b7'],
    }

    def __init__(self, root_note, tuning=list('EADGBE')):

        self.available_scales = list(self.scale_map.keys())
        self.available_appregios = list(self.appregio_map.keys())
        self.tuning = tuning

        # Generate fretboard
        self.root_note = root_note
        self.fretboard = Fretboard(root_note, tuning)

        self.string_names = list(self.fretboard.string_notes_df.index)

    
    def get_notes_and_intervals(self, scale_or_appregio, mode='scale'):

        if mode == 'scale':
            mapping_dict = self.scale_map
            self.mode = 'scale'
        elif mode == 'appregio':
            mapping_dict = self.appregio_map
            self.mode = 'appregio'

        if scale_or_appregio in mapping_dict.keys():
            
            self.scale = scale_or_appregio
            self.scale_appregio_intervals_list = mapping_dict[scale_or_appregio]
            
            scale_appregio_notes = []
            for si in self.scale_appregio_intervals_list:
                for n, iv in self.fretboard.note_interval_map.items():
                    if si in iv:
                        scale_appregio_notes.append(n)
            self.scale_appregio_notes_list = scale_appregio_notes

            if scale_or_appregio == 'Whole Fretboard':
                self.mapped_fretboard_notes = self.fretboard.string_notes_df
                self.mapped_fretboard_intervals = self.fretboard.string_intervals_df
            else:            
                fretboard_match_map = {}
                for interval in mapping_dict[scale_or_appregio]:
                    interval_matches = []      
                    for fret in range(self.fretboard.num_frets):
                        fret_match = self.fretboard.string_intervals_df[fret].apply(lambda x: 1 if interval in x else 0)
                        interval_matches.append(fret_match)
                    
                    fretboard_match_map[interval] = pd.concat(interval_matches, axis=1)

                fmm_keys= list(fretboard_match_map.keys())
                first_interval_df = fretboard_match_map[fmm_keys[0]]
                for k in fmm_keys[1:]:
                    first_interval_df = first_interval_df.add(fretboard_match_map[k])

                self.interval_mask = first_interval_df

                self.mapped_fretboard_notes = self.fretboard.string_notes_df * self.interval_mask
                self.mapped_fretboard_intervals = self.fretboard.string_intervals_df * self.interval_mask
        
        else:
            Exception(f'{self.mode.upper()} not found!')
                    

                        
# def scale_visualizer(sf, root_color, interval_map):

#     scale_df = sf.fretboard_scale_positions
#     strings = list(scale_df.columns)
#     string_num = list(range(len(strings)))
#     strings_dict = {s: n for s,n in zip(strings, string_num)}

#     p = figure(
#         width=1500, 
#         height=200, 
#         x_range=(-0.25, 21.25),
#         x_axis_label = 'FRET',
#         y_range=strings,
#         y_axis_label='STRING'
#     )

#     # ROOTs
#     root_data = scale_df.loc['1']    
#     for s in strings:
#         positions = root_data[s]
#         string = [s for _ in range(len(positions))]
#         p.circle(x=positions, y=string, size=20, line_width=0, fill_color=root_color)

#         for pos, s in zip(positions, string):
#             label = Label(x=pos, y=strings_dict[s], text='1', text_color='white', text_font_size='8pt', text_align='center', y_offset=9)

#             p.add_layout(label)

#     # INTERVALS
#     intervals = [k for k, v in interval_map.items() if v[0]]
#     # interval_colors = []
#     interval_color_map = {k: v[1] for k, v in interval_map.items() if v[0]}
#     for i in intervals:
#         interval_data = scale_df.loc[i]
#         for s in strings:
#             positions = interval_data[s]
#             string = [s for _ in range(len(positions))]
#             p.circle(x=positions, y=string, size=20, line_width=0, fill_color=interval_color_map[i])

#             if i.find('b') > 0:
#                 y_offset = 7
#             else:
#                 y_offset = 9

#             for pos, s in zip(positions, string):
#                 label = Label(x=pos, y=strings_dict[s], text=str(i), text_color='white', text_font_size='8pt', text_align='center', y_offset=y_offset)

#                 p.add_layout(label)

#     p.outline_line_width = 2
#     p.outline_line_color = 'black'
#     p.xaxis.ticker = list(range(0,22))
#     p.ygrid.grid_line_width = 5
#     p.ygrid.grid_line_color = 'black'

#     return p

# # show(p, new='window')