import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer


class ThematicDriftTools:
    """
    Analyzer for thematic alignment / topic evolution workflows.

    Parameters
    ----------
    year_col : str
        Column name in df containing the publication year (int).
    cluster_col : str
        Column name in df containing cluster/topic assignments (int).
    text_col : str
        Column name in df containing cleaned text (string).
    """
    def plot_topic_evolution(self, df, num_clusters):
        evolution = pd.crosstab(df["year"], df["cluster"])
        evolution_pct = evolution.div(evolution.sum(1), axis=0) * 100
        evolution_pct = evolution_pct[evolution_pct.index >= 2015]

        plt.figure(figsize=(8, 6))
        colors = sns.color_palette("viridis", n_colors=num_clusters)

        plt.stackplot(
            evolution_pct.index,
            evolution_pct.T,
            labels=[f"Topic {i}" for i in range(num_clusters)],
            colors=colors,
            alpha=0.85,
        )

        plt.title("Evolution of Medical AI Research Topics (2015-2025)", fontsize=10)
        plt.xlabel("Year", fontsize=10)
        plt.ylabel("Share of Research Output (%)", fontsize=10)
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title="Semantic Topics")
        plt.margins(0, 0)
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
        plt.tight_layout()
        plt.show()

        return evolution_pct

    def extract_top_keywords(self, df, cluster_col="cluster", text_col="clean_text", n_terms=10):
        grouped_text = (
            df.groupby(cluster_col)[text_col]
            .apply(lambda x: " ".join(x))
            .reset_index()
        )

        tfidf = TfidfVectorizer(stop_words="english", max_features=1000)
        tfidf_matrix = tfidf.fit_transform(grouped_text[text_col])
        feature_names = np.array(tfidf.get_feature_names_out())

        topic_keywords = {}
        for i in range(len(grouped_text)):
            row = tfidf_matrix[i].toarray().flatten()
            top_indices = row.argsort()[-n_terms:][::-1]
            top_words = feature_names[top_indices]
            topic_keywords[i] = ", ".join(top_words)

        return topic_keywords

    def generate_summary_report(self, keywords_dict, evolution_df, start_year=2019, end_year=2025):
        report_data = []

        available_years = evolution_df.index.tolist()
        if start_year not in available_years:
            start_year = min(available_years)
        if end_year not in available_years:
            end_year = max(available_years)

        print(f"Analyzing trends from {start_year} to {end_year}...")

        for cluster_id, key_terms in keywords_dict.items():
            try:
                start_share = evolution_df.loc[start_year, cluster_id]
                end_share = evolution_df.loc[end_year, cluster_id]
            except KeyError:
                start_share = evolution_df.iloc[0, cluster_id]
                end_share = evolution_df.iloc[-1, cluster_id]

            change = end_share - start_share

            if change > 2.0:
                status = "Rising"
                trend_score = 1
            elif change < -2.0:
                status = "Falling"
                trend_score = -1
            else:
                status = "STABLE"
                trend_score = 0

            report_data.append(
                {
                    "Topic ID": cluster_id,
                    "Top Keywords (Semantic Signature)": key_terms,
                    f"{start_year}": f"{start_share:.1f}%",
                    f"{end_year}": f"{end_share:.1f}%",
                    "Change": f"{change:+.1f}%",
                    "Status": status,
                    "_sort_val": change,
                }
            )

        summary_df = pd.DataFrame(report_data)
        summary_df = summary_df.sort_values(by="_sort_val", ascending=False).drop(columns=["_sort_val"])
        return summary_df
