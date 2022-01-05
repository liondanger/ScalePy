import streamlit as st
from scales import *

st.set_page_config(
    page_title="ScalePy",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

selected_root_note = st.sidebar.selectbox('Select Root Note', notes)
scale_finder = ScaleFinder(selected_root_note)

root_highlight_color = st.sidebar.color_picker('Select Root Note Highlight Color', '#ff0000')

selected_scale_appregio_mode = st.sidebar.radio('Scale or Appregio', ['Scale', 'Appregio'])

if selected_scale_appregio_mode == 'Scale':
    selected_scale = st.sidebar.selectbox('Select Scale', scale_finder.available_scales)
    scale_finder.get_notes_and_intervals(selected_scale, mode='scale')
else:
    selected_scale = st.sidebar.selectbox('Select Appregio', scale_finder.available_appregios)
    scale_finder.get_notes_and_intervals(selected_scale, mode='appregio')

# Capture chosen scale notes and intervals for easy access
scale_notes = scale_finder.mapped_fretboard_notes
scale_notes_list = scale_finder.scale_appregio_notes_list
scale_intervals = scale_finder.mapped_fretboard_intervals
scale_intervals_list = scale_finder.scale_appregio_intervals_list
fretboard_tuning = scale_finder.tuning

string_nums = list(range(1,7))
string_nums.reverse()
tuning_fmt = [f'{string_note}{string_num}' for string_note, string_num in zip(fretboard_tuning, string_nums)]

st.markdown(
    f"<h2>{selected_scale} {scale_finder.mode.title()} | Root: {selected_root_note}</h2>",
    unsafe_allow_html=True
)

# toggle_custom_tuning = st.checkbox('Custom Tuning?')
# if toggle_custom_tuning:
#     string_numbers = list('654321')
#     # string_numbers.reverse()
#     string_numbers
#     custom_tuning_columns = st.columns(len(string_numbers))
#     custom_tuning_map = {}
#     for i in string_numbers:
#         with custom_tuning_columns[int(i)-1]:
#             custom_string_tuning = st.selectbox(f'String {i} Tuning', notes, key=f'custom_tuned_string_{i}')
#             custom_tuning_map[i] = custom_string_tuning
#     custom_tuning_map
#     custom_tuning = list(custom_tuning_map.values())
#     custom_tuning

st.markdown(f"**_Tuning_**: {' | '.join(fretboard_tuning)}")

note_interval_df = pd.DataFrame()
note_interval_df['Interval'] = scale_intervals_list
note_interval_df['Note'] = scale_notes_list
st.sidebar.table(note_interval_df.set_index('Interval'))

spaces = ' ' * 20
fret_fmt = [f'{spaces}{f}' for f in range(24)]

strings = tuning_fmt
p = figure(
    width=1500, 
    height=200, 
    x_range=(0.25, 23.9),
    x_axis_label = 'FRET',
    y_range=strings,
    y_axis_label='STRING',
    toolbar_location=None
)

color_map = [
    # '#802130',
    root_highlight_color,
    # '#ff0000',
    '#ffa500',
    '#cccc00',
    '#008000',
    '#0000ff',
    '#4b0082',
    '#ee82ee',
    '#e5175f',
    '#d89e00',
    '#b7d15b',
    '#9fefaf',
    '#24586d',
    '#388dac',
    '#4bcdf5',
    '#4bcdf5',
    '#4bcdf5',
    '#4bcdf5',
    '#4bcdf5',
]

def get_color_for_note_interval(type, value):
    if type == 'note':
        ix = scale_notes_list.index(value)
        return color_map[ix]
    elif type == 'interval':
        ix = scale_intervals_list.index(value)
        return color_map[ix]
    else:
        Exception('type must be "note" or "interval".')

st.markdown('<hr>', unsafe_allow_html=True)

fretboard_fmt_columns = st.columns(4)

with fretboard_fmt_columns[0]:
    selected_fret_label = st.selectbox('Label With', ['Note', 'Interval'])
    selected_fret_label = selected_fret_label.lower()

# if selected_fret_label == 'interval':
#     with fretboard_fmt_columns[1]:
#         selected_fret_interval_type = st.selectbox('Interval Type', ['Flat', 'Sharp'])
#         selected_fret_interval_type = selected_fret_interval_type.lower()

# selected_fret_label = 'note'
selected_fret_interval_type = 'flat'

custom_labels = {x: y for x, y in zip(list(scale_notes.columns), fret_fmt)}

with fretboard_fmt_columns[1]:
    selected_fret_filter_mode = st.selectbox('Fret Filter Mode', ['Range', 'List'])

with fretboard_fmt_columns[2]:
    if selected_fret_filter_mode == 'Range':
        selected_frets = st.slider('Filter Frets', min_value=0, max_value=23, value=(0,23))
        selected_frets = list(range(selected_frets[0], selected_frets[1] + 1))
        # st.write(list(range(selected_frets[0], selected_frets[1] + 1)))
    else:
        selected_frets = st.multiselect('Filter Frets', list(range(24)))
        # selected_frets
        if selected_frets == []:
            selected_frets = list(range(24))
        else:
            selected_frets = [int(f) for f in selected_frets]
        # selected_frets

with fretboard_fmt_columns[3]:    
    selected_strings = st.multiselect('Filter Strings', tuning_fmt)
    if selected_strings == []:
        selected_strings = tuning_fmt
    string_reverse_lookup = {s: i for s, i in zip(tuning_fmt, range(6))}
    selected_strings = [string_reverse_lookup[s] for s in selected_strings]

def note_interval_highlight_widget(note):

    ix = scale_notes_list.index(note)
    corresponding_interval = scale_intervals_list[ix]

    st.markdown(f'**{note} | {corresponding_interval}**')
    chosen_color = st.color_picker('Highlight Color', color_map[ix], key=f'{ix}_{note}_cp')

    return ix, chosen_color

with st.expander('Edit Highlight Colors'):
    
    color_choser_cols = st.columns(len(scale_notes_list))
    for ix, note in enumerate(scale_notes_list):         
        with color_choser_cols[ix]:
            ix, highlight_color = note_interval_highlight_widget(note)
            color_map[ix] = highlight_color

for i in range(6):
    for j in range(24):
        current_note = scale_notes.iloc[i, j]

        if current_note != '':            

            if selected_fret_label == 'interval':
            
                if selected_fret_interval_type == 'flat':
                    label_text = str(scale_intervals.iloc[i, j][0])
                else:
                    label_text = str(scale_intervals.iloc[i, j][1])
            
                y_offset = 8

            else:
                label_text = current_note
                y_offset = 6

            if (j in selected_frets) & (i in selected_strings):
                p.circle(x=j+0.5, y=i+0.5, size=20, line_width=0, fill_color=get_color_for_note_interval(selected_fret_label, label_text))
                label = Label(x=j, y=i, text=label_text, text_color='white', text_font_size='8pt', text_align='center', x_offset=30.5, y_offset=y_offset)
                p.add_layout(label)

p.outline_line_width = 2
p.outline_line_color = 'black'

p.xaxis.ticker = list(range(0,25))
p.xaxis.major_label_overrides = custom_labels
p.xaxis.axis_label_text_font_style = "bold"

p.ygrid.grid_line_width = 4
p.ygrid.grid_line_color = 'black'
p.yaxis.axis_label_text_font_style = "bold"

p.toolbar.active_drag = None

st.markdown('<hr>', unsafe_allow_html=True)

st.bokeh_chart(p)

# show_interval_map = {}
# for sic in range(len(scale_intervals)):

#     si = scale_intervals[sic]
#     # with scale_interval_cols[sic]:
#     show_interval = st.sidebar.checkbox(si, value=True, key=f'checkbox_{selected_scale}_{si}')
#     interval_color = st.side.bar.color_picker('Highlight color', value=default_colors[sic], key=f'color_{selected_scale}_{si}')

#     show_interval_map[si] = [show_interval, interval_color]
# show_interval_map
# [k for k, v in show_interval_map.items() if v[0]]


# root_scale_col_0, root_scale_col_1 = st.columns(2)
# with root_scale_col_0:
#     root_note = st.selectbox('Choose Root Note', notes)

# with root_scale_col_1:
#     scale = st.selectbox('Choose Scale', list(scale_map.keys()))

# st.header(f'{root_note} {scale} Scale')

# scale_data = ScaleFinder(Fretboard(root_note), scale, scale_map)
# scale_data

# root_color = st.color_picker('Root highlight color', value='#D42512')
# default_colors = [
#     '#ffb913',
#     '#ff6213',
#     '#811059',
#     '#ff1398',
#     '#381334',
#     '#26675d',
#     '#108138',
#     '#264167',
#     '#13affe',
#     '#262867',
#     '#201338', 
# ]

# scale_intervals = list(scale_data.fretboard_scale_positions.index)[1:]
# st.markdown('**Select Intervals to Show**')
# scale_interval_cols = st.columns(len(scale_intervals))

# show_interval_map = {}
# for sic in range(len(scale_intervals)):

#     si = scale_intervals[sic]
#     with scale_interval_cols[sic]:
#         show_interval = st.checkbox(si, value=True, key=f'checkbox_{scale}_{si}')
#         interval_color = st.color_picker('Highlight color', value=default_colors[sic], key=f'color_{scale}_{si}')
    
#         show_interval_map[si] = [show_interval, interval_color]
# # show_interval_map
# # [k for k, v in show_interval_map.items() if v[0]]

# st.subheader('Fretboard')
# scale_viz = scale_visualizer(scale_data, root_color, show_interval_map)
# st.bokeh_chart(scale_viz)