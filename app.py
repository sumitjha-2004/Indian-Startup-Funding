import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')
# Load the dataset
df = pd.read_csv('startup_clean.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
# Get the single list of unique, cleaned, and sorted investors
unique_investors = sorted(df['Investors'].dropna().str.split(',').explode().str.strip().unique().tolist())


def load_investor_detail(investor):
    st.title(investor)
    st.divider()
    # load resent 5 investments
    resent5_df = df[df['Investors'].str.contains(investor)].sort_values(by='Date', ascending=False).head()[
        ['Date', 'Startup', 'Industry', 'SubVertical', 'City', 'InvestmentType', 'amount(cr.)']]
    st.subheader('Most resent 5 Investment :')
    st.dataframe(resent5_df)
    st.divider()

    # bigest Investment
    col1, col2 = st.columns(2)
    with col1:
        big_df = df[df['Investors'].str.contains(investor, regex=False, na=False)] \
            .groupby('Startup')['amount(cr.)'].sum().sort_values(ascending=False).head()

        st.subheader('Top 5 Investments')

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(big_df.index, big_df.values, color='#2E86AB', width=0.6)

        # add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.1f}',
                ha='center', va='bottom',
                fontsize=9, fontweight='bold'
            )

        ax.set_xlabel('Startup', fontsize=11)
        ax.set_ylabel('Amount (Cr.)', fontsize=11)
        ax.set_title('Top 5 Investments by Amount', fontsize=13, fontweight='bold')

        plt.xticks(rotation=30, ha='right', fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', linestyle='--', alpha=0.4)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    with col2:
        st.subheader('Most biggest 5 Investment data:')
        st.dataframe(big_df)

    st.divider()
    # verticlas of investments
    # --- Row 1: Sector & Investment Type ---
    col1, col2 = st.columns(2)

    with col1:
        vertical_df = df[df['Investors'].str.contains(investor, regex=False, na=False)] \
            .groupby('SubVertical')['amount(cr.)'].sum().sort_values(ascending=False).head()

        st.subheader('Sector Invested In')

        fig, ax = plt.subplots(figsize=(5, 5))
        colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#6C5CE7', '#FF8C42']
        wedges, texts, autotexts = ax.pie(
            vertical_df,
            labels=None,
            autopct='%0.1f%%',
            startangle=90,
            colors=colors,
            pctdistance=0.8,
            explode=[0.05] * len(vertical_df),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        plt.setp(autotexts, size=9, weight='bold', color='white')
        ax.legend(
            wedges, vertical_df.index,
            loc='center left', bbox_to_anchor=(1, 0.5),
            fontsize=9, frameon=False
        )
        ax.set_title('Sector Distribution', fontsize=13, fontweight='bold', color='#333333')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col2:
        round_df = df[df['Investors'].str.contains(investor, regex=False, na=False)] \
            .groupby('InvestmentType')['amount(cr.)'].sum().sort_values(ascending=False).head()

        st.subheader('Investment Type')

        fig, ax = plt.subplots(figsize=(5, 5))
        colors = ['#F72585', '#4CC9F0', '#7209B7', '#3A86FF', '#FB5607']
        wedges, texts, autotexts = ax.pie(
            round_df,
            labels=None,
            autopct='%0.1f%%',
            startangle=90,
            colors=colors,
            pctdistance=0.8,
            explode=[0.05] * len(round_df),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        plt.setp(autotexts, size=9, weight='bold', color='white')
        ax.legend(
            wedges, round_df.index,
            loc='center left', bbox_to_anchor=(1, 0.5),
            fontsize=9, frameon=False
        )
        ax.set_title('Investment Type Split', fontsize=13, fontweight='bold', color='#333333')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    st.divider()
    # --- Row 2: Year on Year & City ---
    col1, col2 = st.columns(2)

    with col1:
        year_df = df[df['Investors'].str.contains(investor, regex=False, na=False)] \
            .groupby('year')['amount(cr.)'].sum()

        st.subheader('Year on Year Investment')

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(
            year_df.index, year_df.values,
            marker='o', linewidth=3, markersize=9,
            color='#F72585', markerfacecolor='#FFD93D',
            markeredgecolor='#F72585', markeredgewidth=2
        )
        ax.fill_between(year_df.index, year_df.values, alpha=0.25, color='#4CC9F0')
        ax.set_xlabel('Year', fontsize=10)
        ax.set_ylabel('Amount (Cr.)', fontsize=10)
        ax.set_title('Investment Trend', fontsize=13, fontweight='bold', color='#333333')
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticks(year_df.index)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col2:
        city_df = df[df['Investors'].str.contains(investor, regex=False, na=False)] \
            .groupby('City')['amount(cr.)'].sum().sort_values(ascending=False).head()

        st.subheader('Top Cities')

        fig, ax = plt.subplots(figsize=(5, 5))
        colors = ['#06D6A0', '#EF476F', '#FFD166', '#118AB2', '#8338EC']
        wedges, texts, autotexts = ax.pie(
            city_df,
            labels=None,
            autopct='%0.1f%%',
            startangle=90,
            colors=colors,
            pctdistance=0.8,
            explode=[0.05] * len(city_df),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        plt.setp(autotexts, size=9, weight='bold', color='white')
        ax.legend(
            wedges, city_df.index,
            loc='center left', bbox_to_anchor=(1, 0.5),
            fontsize=9, frameon=False
        )
        ax.set_title('City-wise Distribution', fontsize=13, fontweight='bold', color='#333333')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)


def load_overall_analysis():
    st.title('Overall Analysis')
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Total Invested amount
        total = round(df['amount(cr.)'].sum())
        st.metric('Total Amount Invested', str(total) + ' cr')
    with col2:
        # Highest Investment amount
        highest =  round(df.groupby('Startup')['amount(cr.)'].max().sort_values(ascending=False).head(1).values[0])
        st.metric('maximum Amount Invested', str(highest)+ ' cr')
    with col3:
        avg = round(df.groupby('Startup')['amount(cr.)'].sum().mean())
        st.metric('Avg Amount Invested', str(avg) + ' cr')
    with col4:
        unique = df['Startup'].nunique()
        st.metric('Number of Startup', str(unique) )
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        # Month on Month graph
        st.header('Month on Month Graph')
        selected_option_1 = st.selectbox('Select Type', ['Total Amount', 'count'], key='mom_type')

        if selected_option_1 == 'Total Amount':
            temp_df = df.groupby(['year', 'month'])['amount(cr.)'].sum().reset_index()
        else:
            temp_df = df.groupby(['year', 'month'])['amount(cr.)'].count().reset_index()

        temp_df = temp_df.sort_values(['year', 'month'])
        temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(
            temp_df['x_axis'],
            temp_df['amount(cr.)'],
            marker='o',
            linewidth=2,
            markersize=5,
            color='#2E86AB'
        )
        ax.set_xlabel('Month-Year', fontsize=10)
        ax.set_ylabel('Amount (Cr.)' if selected_option_1 == 'Total Amount' else 'Number of Deals', fontsize=10)
        ax.set_title(f'Month on Month {selected_option_1}', fontsize=12, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.4)
        plt.xticks(rotation=60, ha='right', fontsize=7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col2:
        # Industry pie chart
        st.header('Investment by Industry')
        selected_option_2 = st.selectbox('Select Type', ['Total Amount', 'count'], key='industry_type')

        if selected_option_2 == 'Total Amount':
            industry_df = df.groupby('Industry')['amount(cr.)'].sum().sort_values(ascending=False)
        else:
            industry_df = df.groupby('Industry')['amount(cr.)'].count().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(7, 5))
        colors = plt.cm.tab20.colors
        wedges, texts, autotexts = ax.pie(
            industry_df,
            labels=None,
            autopct='%0.1f%%',
            startangle=90,
            colors=colors[:len(industry_df)],
            pctdistance=0.8,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        plt.setp(autotexts, size=7, weight='bold', color='white')
        ax.legend(
            wedges, industry_df.index,
            title='Industry',
            loc='center left', bbox_to_anchor=(1, 0.5),
            fontsize=7, frameon=False
        )
        ax.set_title(f'Industry Distribution ({selected_option_2})', fontsize=12, fontweight='bold', color='#333333')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        # 1. Type of Funding
        st.subheader('Type of Funding')

        investment_type_df = df.groupby('InvestmentType')['amount(cr.)'].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(7, 5))
        colors = plt.cm.tab20.colors
        wedges, texts, autotexts = ax.pie(
            investment_type_df,
            labels=None,
            autopct='%0.1f%%',
            startangle=90,
            colors=colors[:len(investment_type_df)],
            pctdistance=0.8,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        plt.setp(autotexts, size=7, weight='bold', color='white')
        ax.legend(
            wedges, investment_type_df.index,
            title='Investment Type',
            loc='center left', bbox_to_anchor=(1, 0.5),
            fontsize=7, frameon=False
        )
        ax.set_title('Funding by Type', fontsize=12, fontweight='bold', color='#333333')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with col2:
        # 2. City wise Funding
        st.subheader('City wise Funding')

        city_df = df.groupby('City')['amount(cr.)'].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(7, 5))
        colors = plt.cm.tab20.colors
        wedges, texts, autotexts = ax.pie(
            city_df,
            labels=None,
            autopct='%0.1f%%',
            startangle=90,
            colors=colors[:len(city_df)],
            pctdistance=0.8,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
        )
        plt.setp(autotexts, size=7, weight='bold', color='white')
        ax.legend(
            wedges, city_df.index,
            title='City',
            loc='center left', bbox_to_anchor=(1, 0.5),
            fontsize=7, frameon=False
        )
        ax.set_title('Funding by City', fontsize=12, fontweight='bold', color='#333333')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    st.divider()
    st.subheader('Top Startups')

    year_option = st.selectbox(
        'Select Year',
        ['Overall'] + sorted(df['year'].unique().tolist()),
        key='top_startup_year'
    )

    if year_option == 'Overall':
        top_startups_df = df.groupby('Startup')['amount(cr.)'].sum().sort_values(ascending=False).head()
    else:
        top_startups_df = df[df['year'] == year_option] \
            .groupby('Startup')['amount(cr.)'].sum().sort_values(ascending=False).head()

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.tab20.colors
    bars = ax.bar(top_startups_df.index, top_startups_df.values, color=colors[:len(top_startups_df)])

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height:.1f}',
            ha='center', va='bottom',
            fontsize=9, fontweight='bold'
        )

    ax.set_xlabel('Startup', fontsize=11)
    ax.set_ylabel('Amount (Cr.)', fontsize=11)
    ax.set_title(f'Top Startups - {year_option}', fontsize=13, fontweight='bold')
    plt.xticks(rotation=30, ha='right', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)



def load_startup_detail(startup):
    startup_df = df[df['Startup'] == startup]

    st.title(startup)

    industry = startup_df['Industry'].dropna().unique()
    subindustry = startup_df['SubVertical'].dropna().unique()
    location = startup_df['City'].dropna().unique()

    st.caption(', '.join(industry) if len(industry) > 0 else 'Industry Not Available')

    st.divider()

    st.header("Company Overview")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Industry :")
        st.write(', '.join(industry) if len(industry) > 0 else 'Not Available')

        st.subheader("Subindustry :")
        st.write(', '.join(subindustry) if len(subindustry) > 0 else 'Not Available')

    with col2:
        st.subheader("Founders :")
        st.write('Not Available')

        st.subheader("Location :")
        st.write(', '.join(location) if len(location) > 0 else 'Not Available')

    st.divider()
    # Quick stats row above the table
    total_raised = startup_df['amount(cr.)'].sum()
    num_rounds = startup_df['Date'].nunique()
    latest_round = startup_df.sort_values(by='Date', ascending=False)['InvestmentType'].iloc[
        0] if not startup_df.empty else 'N/A'

    s1, s2, s3 = st.columns(3)
    s1.metric("Total Raised", f"₹{total_raised:,.1f} Cr.")
    s2.metric("Funding Rounds", num_rounds)
    s3.metric("Latest Round", latest_round)

    st.subheader('Funding History')
    funding_rounds_df = startup_df[['Date', 'InvestmentType', 'Investors', 'amount(cr.)']] \
        .sort_values(by='Date', ascending=False) \
        .rename(columns={
        'InvestmentType': 'Stage',
        'amount(cr.)': 'Amount (Cr.)'
    })

    st.dataframe(
        funding_rounds_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Amount (Cr.)": st.column_config.NumberColumn(
                "Amount (Cr.)", format="₹%.2f Cr."
            ),
            "Date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
        }
    )





st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investors'])

if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        st.session_state['show_overall'] = True

    if st.session_state.get('show_overall', False):
        load_overall_analysis()
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Detail')
    if btn1:
        load_startup_detail(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor',unique_investors)
    btn2 = st.sidebar.button('Find Investor Detail')
    if btn2:
        load_investor_detail(selected_investor)
