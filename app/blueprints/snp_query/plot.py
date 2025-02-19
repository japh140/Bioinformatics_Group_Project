from flask import Blueprint, render_template, session
import matplotlib.pyplot as plt
import io
import base64

try:
    # absolute import version
    from app.blueprints.snp_query.views import snp_bp
    from app.blueprints.db_api.db_api import db
except ImportError:
    # relative import version
    from views import snp_bp
    from ..db_api.db_api import db


plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/plot-fst', methods=['GET', 'POST'])  # Allow both GET and POST
def plot_fst():
    print("Entered plot_fst route!")  # Debug: Print entry to the route
    try:
        # Retrieve the FST data from the session
        fst_data = session.get('fst_data', [])
        print(f"Retrieved FST data from session: {fst_data}")

        if not fst_data:
            print("No FST data found in session.")
            raise ValueError("No FST data found in session.")

        # Filter the data to get SNP IDs and their corresponding FST values for the plot
        snp_ids_for_plot = [item['snp_id'] for item in fst_data if item['fst'] != 'N/A']
        fst_values_for_plot = [item['fst'] for item in fst_data if item['fst'] != 'N/A']

        print(f"SNP IDs for plot: {snp_ids_for_plot}")
        print(f"FST values for plot: {fst_values_for_plot}")

        if not fst_values_for_plot:
            print("No valid FST values to plot.")
            return render_template('error.html', message="No valid FST values to plot.")

        # Set a fixed bar width
        bar_width = 0.5  # Adjust this value as needed

        # Adjust figure size based on the number of bars
        num_bars = len(fst_values_for_plot)
        if num_bars == 1:
            fig_width = 4  # Smaller width for single bar
        else:
            fig_width = max(6, num_bars * 1.5)  # Adjust width for multiple bars

        # Create a bar plot
        plt.figure(figsize=(fig_width, 6))  # Adjust figure size dynamically
        bars = plt.bar(snp_ids_for_plot, fst_values_for_plot, color='cadetblue', width=bar_width)

        # Adjust x-axis limits to ensure bars are properly spaced
        if num_bars == 1:
            plt.xlim(-0.5, 0.5)  # Center the single bar
        else:
            plt.xlim(-0.5, num_bars - 0.5)  # Center multiple bars

        # Add labels and title
        plt.xlabel('SNP ID')
        plt.ylabel('FST Value')
        plt.title('FST Values for Selected SNPs')

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')  # Use bbox_inches='tight' to avoid cropping
        img.seek(0)

        # Convert the image to base64
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        # Render the population comparison template with the plot
        return render_template('homepage/population_comparison.html',
                               fst_plot=f"data:image/png;base64,{img_base64}",
                               populations={item['snp_id']: {'fst': item['fst']} for item in fst_data},
                               snp_ids=snp_ids_for_plot,
                               message="Population comparison statistics are displayed below.")

    except Exception as e:
        print(f"Error generating plot: {e}")
        return render_template('error.html', message=f"Error generating plot: {e}")