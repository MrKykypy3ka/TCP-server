import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


def create_custom_colormap(colors):
    colormap = ListedColormap(colors)
    return colormap


def save_pivot_table_as_image(pivot_table, file_path, cmap='YlGnBu', name_table='Сводная таблица'):
    fig, ax = plt.subplots(figsize=(10, 6))
    heatmap = ax.imshow(pivot_table, cmap=cmap)

    ax.set_xticks(range(len(pivot_table.columns)))
    ax.set_yticks(range(len(pivot_table.index)))
    ax.set_xticklabels(pivot_table.columns)
    ax.set_yticklabels(pivot_table.index)
    ax.set_xlabel('Date')
    ax.set_ylabel('Area, Type of Road')
    ax.set_title(name_table)

    cbar = plt.colorbar(heatmap)
    cbar.set_label('Значения')

    for i in range(len(pivot_table.index)):
        for j in range(len(pivot_table.columns)):
            value = pivot_table.iloc[i, j]
            ax.text(j, i, f'{value:.3f}', ha='center', va='center', color='black')

    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close()