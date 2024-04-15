import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins

from pathlib import Path

# Load Palmer Penguins DataFrame
df = palmerpenguins.load_penguins()

# Set page title
ui.page_opts(title="Penguins dashboard", fillable=True)

# Create sidebar
with ui.sidebar(title="Filter controls"):
    # Slider: select mass between 2000 and 6000 grams
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Checkbox group: select species (default: all selected)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    # Links to GitHub sources and other references
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Container with 3 value boxes. Contents will wrap to next row when the screen is narrow.
with ui.layout_column_wrap(fill=False):
    # Displays the number of penguins in the filtered dataframe
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    # Displays the average bill length of the penguins in the filtered dataframe
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Displays the average pill depth of the penguins in the filtered dataframe
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Container with a scatter plot and a data frame
with ui.layout_columns():
    # Scatter plot of the filtered data frame
        # Compares bill length and bill depth
        # Species are indicated by color with a legend
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Displays filtered data frame
        # Includes species, island, bill length, bill depth, and body mass
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Set text style using CSS
ui.include_css(
    Path(__file__).parent / "styles.css"
)

# Reactive calc function to filter data frame when input.species() or input.mass() is changed.
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
