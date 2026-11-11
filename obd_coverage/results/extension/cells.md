# Every cell of the extension

Written by `python -m obd_coverage.extension_tables` from `coverage.json`. "Interval below" is the share of intervals that lie below the true value.

| Campaign | Scenario | Quantity | Unit | Coverage | Wilson 95% | Label | Interval contains 0.95 | Predicted | Prediction inside | Interval below | Interval above | Mean width | Median width | sd of replicates / sd of estimate | Coverage of mean estimate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All | F | ips_ratio | rows | 0.905 | 0.895 to 0.913 | under-covers | no | 0.912 | yes | 0.054 | 0.041 | 0.127 | 0.127 | 0.855 | 0.906 |
| All | F | ips_ratio | impressions | 0.910 | 0.900 to 0.918 | under-covers | no | 0.916 | yes | 0.052 | 0.038 | 0.129 | 0.129 | 0.868 | 0.908 |
| All | F | ips_ratio | 5 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.033 | 0.021 | 0.148 | 0.147 | 0.994 | 0.946 |
| All | F | ips_ratio | 10 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.953 | no | 0.033 | 0.022 | 0.148 | 0.147 | 0.994 | 0.945 |
| All | F | ips_ratio | 20 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.033 | 0.021 | 0.148 | 0.148 | 0.996 | 0.946 |
| All | F | ips_ratio | 30 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.034 | 0.020 | 0.148 | 0.148 | 0.999 | 0.946 |
| All | F | ips_ratio | 60 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.033 | 0.020 | 0.148 | 0.148 | 0.997 | 0.946 |
| All | F | ips_ratio | 180 min | 0.942 | 0.934 to 0.948 | adequate | no | 0.955 | no | 0.034 | 0.025 | 0.147 | 0.147 | 0.993 | 0.942 |
| All | F | snips_ratio | rows | 0.905 | 0.895 to 0.913 | under-covers | no | 0.911 | yes | 0.054 | 0.042 | 0.127 | 0.127 | 0.853 | 0.905 |
| All | F | snips_ratio | impressions | 0.908 | 0.899 to 0.917 | under-covers | no | 0.916 | yes | 0.052 | 0.039 | 0.129 | 0.128 | 0.866 | 0.908 |
| All | F | snips_ratio | 5 min | 0.942 | 0.935 to 0.949 | adequate | no | 0.949 | no | 0.035 | 0.023 | 0.145 | 0.145 | 0.980 | 0.943 |
| All | F | snips_ratio | 10 min | 0.942 | 0.934 to 0.949 | adequate | no | 0.950 | no | 0.035 | 0.023 | 0.145 | 0.145 | 0.979 | 0.942 |
| All | F | snips_ratio | 20 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.950 | yes | 0.035 | 0.022 | 0.146 | 0.146 | 0.982 | 0.944 |
| All | F | snips_ratio | 30 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.950 | no | 0.035 | 0.021 | 0.146 | 0.145 | 0.982 | 0.943 |
| All | F | snips_ratio | 60 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.951 | no | 0.034 | 0.024 | 0.146 | 0.145 | 0.982 | 0.942 |
| All | F | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.952 | no | 0.034 | 0.027 | 0.146 | 0.145 | 0.981 | 0.940 |
| All | F | ips | rows | 0.907 | 0.898 to 0.916 | under-covers | no | 0.915 | yes | 0.054 | 0.039 | 0.000625 | 0.000624 | 0.867 | 0.908 |
| All | F | ips | impressions | 0.910 | 0.901 to 0.919 | under-covers | no | 0.920 | no | 0.052 | 0.037 | 0.000634 | 0.000633 | 0.879 | 0.911 |
| All | F | ips | 5 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.035 | 0.019 | 0.000719 | 0.000718 | 0.998 | 0.947 |
| All | F | ips | 10 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.953 | no | 0.035 | 0.021 | 0.000718 | 0.000715 | 0.996 | 0.945 |
| All | F | ips | 20 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.954 | yes | 0.033 | 0.020 | 0.000719 | 0.000716 | 0.998 | 0.947 |
| All | F | ips | 30 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.954 | no | 0.034 | 0.020 | 0.00072 | 0.000718 | 0.999 | 0.947 |
| All | F | ips | 60 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.954 | no | 0.035 | 0.020 | 0.000718 | 0.000715 | 0.996 | 0.945 |
| All | F | ips | 180 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.953 | no | 0.035 | 0.025 | 0.000711 | 0.000708 | 0.987 | 0.941 |
| All | F | v_on | rows | 0.732 | 0.718 to 0.746 | under-covers | no | 0.716 | no | 0.138 | 0.130 | 7.81e-05 | 7.81e-05 | 0.554 | 0.732 |
| All | F | v_on | impressions | 0.766 | 0.752 to 0.779 | under-covers | no | 0.753 | yes | 0.119 | 0.115 | 8.44e-05 | 8.43e-05 | 0.598 | 0.766 |
| All | F | v_on | 5 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.942 | yes | 0.030 | 0.031 | 0.000138 | 0.000138 | 0.978 | 0.938 |
| All | F | v_on | 10 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.950 | yes | 0.029 | 0.025 | 0.000143 | 0.000143 | 1.012 | 0.947 |
| All | F | v_on | 20 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.957 | yes | 0.023 | 0.023 | 0.000147 | 0.000147 | 1.042 | 0.954 |
| All | F | v_on | 30 min | 0.957 | 0.950 to 0.962 | adequate | yes | 0.961 | yes | 0.023 | 0.021 | 0.00015 | 0.00015 | 1.063 | 0.957 |
| All | F | v_on | 60 min | 0.964 | 0.958 to 0.970 | adequate | no | 0.971 | no | 0.019 | 0.017 | 0.000158 | 0.000158 | 1.118 | 0.964 |
| All | F | v_on | 180 min | 0.980 | 0.975 to 0.984 | unresolved | no | 0.987 | no | 0.012 | 0.009 | 0.000176 | 0.000176 | 1.249 | 0.980 |
| All | FH | ips_ratio | rows | 0.848 | 0.837 to 0.859 | under-covers | no | 0.852 | yes | 0.079 | 0.073 | 0.127 | 0.127 | 0.731 | 0.849 |
| All | FH | ips_ratio | impressions | 0.856 | 0.845 to 0.867 | under-covers | no | 0.858 | yes | 0.076 | 0.068 | 0.129 | 0.129 | 0.742 | 0.856 |
| All | FH | ips_ratio | 5 min | 0.909 | 0.900 to 0.918 | under-covers | no | 0.911 | yes | 0.049 | 0.042 | 0.15 | 0.149 | 0.860 | 0.908 |
| All | FH | ips_ratio | 10 min | 0.914 | 0.905 to 0.922 | under-covers | no | 0.917 | yes | 0.046 | 0.040 | 0.152 | 0.151 | 0.873 | 0.914 |
| All | FH | ips_ratio | 20 min | 0.925 | 0.916 to 0.933 | unresolved | no | 0.925 | yes | 0.040 | 0.035 | 0.156 | 0.155 | 0.896 | 0.924 |
| All | FH | ips_ratio | 30 min | 0.932 | 0.924 to 0.939 | unresolved | no | 0.932 | yes | 0.036 | 0.033 | 0.16 | 0.159 | 0.919 | 0.931 |
| All | FH | ips_ratio | 60 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.942 | yes | 0.032 | 0.028 | 0.166 | 0.165 | 0.952 | 0.941 |
| All | FH | ips_ratio | 180 min | 0.942 | 0.934 to 0.949 | adequate | no | 0.950 | no | 0.030 | 0.028 | 0.17 | 0.169 | 0.975 | 0.940 |
| All | FH | snips_ratio | rows | 0.848 | 0.837 to 0.859 | under-covers | no | 0.851 | yes | 0.080 | 0.072 | 0.127 | 0.127 | 0.729 | 0.848 |
| All | FH | snips_ratio | impressions | 0.854 | 0.842 to 0.864 | under-covers | no | 0.857 | yes | 0.078 | 0.069 | 0.129 | 0.129 | 0.740 | 0.852 |
| All | FH | snips_ratio | 5 min | 0.903 | 0.894 to 0.912 | under-covers | no | 0.907 | yes | 0.052 | 0.044 | 0.147 | 0.147 | 0.848 | 0.904 |
| All | FH | snips_ratio | 10 min | 0.911 | 0.902 to 0.919 | under-covers | no | 0.912 | yes | 0.048 | 0.041 | 0.15 | 0.15 | 0.861 | 0.910 |
| All | FH | snips_ratio | 20 min | 0.921 | 0.912 to 0.929 | unresolved | no | 0.921 | yes | 0.043 | 0.036 | 0.154 | 0.154 | 0.885 | 0.920 |
| All | FH | snips_ratio | 30 min | 0.928 | 0.919 to 0.935 | unresolved | no | 0.928 | yes | 0.038 | 0.034 | 0.158 | 0.157 | 0.906 | 0.927 |
| All | FH | snips_ratio | 60 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.939 | yes | 0.033 | 0.029 | 0.164 | 0.163 | 0.940 | 0.937 |
| All | FH | snips_ratio | 180 min | 0.941 | 0.933 to 0.947 | adequate | no | 0.948 | no | 0.030 | 0.029 | 0.168 | 0.167 | 0.966 | 0.939 |
| All | FH | ips | rows | 0.869 | 0.858 to 0.879 | under-covers | no | 0.870 | yes | 0.069 | 0.062 | 0.000625 | 0.000624 | 0.761 | 0.868 |
| All | FH | ips | impressions | 0.876 | 0.865 to 0.886 | under-covers | no | 0.875 | yes | 0.065 | 0.059 | 0.000634 | 0.000634 | 0.771 | 0.875 |
| All | FH | ips | 5 min | 0.916 | 0.907 to 0.924 | under-covers | no | 0.922 | yes | 0.046 | 0.038 | 0.000726 | 0.000725 | 0.884 | 0.915 |
| All | FH | ips | 10 min | 0.923 | 0.914 to 0.931 | unresolved | no | 0.925 | yes | 0.042 | 0.035 | 0.000735 | 0.000733 | 0.894 | 0.922 |
| All | FH | ips | 20 min | 0.924 | 0.916 to 0.932 | unresolved | no | 0.931 | yes | 0.042 | 0.034 | 0.000749 | 0.000747 | 0.911 | 0.924 |
| All | FH | ips | 30 min | 0.931 | 0.923 to 0.938 | unresolved | no | 0.937 | yes | 0.037 | 0.032 | 0.000765 | 0.000762 | 0.930 | 0.930 |
| All | FH | ips | 60 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.944 | yes | 0.034 | 0.026 | 0.000785 | 0.000781 | 0.954 | 0.938 |
| All | FH | ips | 180 min | 0.936 | 0.928 to 0.943 | adequate | no | 0.950 | no | 0.034 | 0.030 | 0.000796 | 0.000792 | 0.968 | 0.937 |
| All | FH | v_on | rows | 0.414 | 0.399 to 0.430 | under-covers | no | 0.424 | yes | 0.292 | 0.293 | 7.81e-05 | 7.8e-05 | 0.283 | 0.416 |
| All | FH | v_on | impressions | 0.438 | 0.423 to 0.453 | under-covers | no | 0.454 | no | 0.280 | 0.282 | 8.43e-05 | 8.43e-05 | 0.306 | 0.439 |
| All | FH | v_on | 5 min | 0.703 | 0.688 to 0.716 | under-covers | no | 0.712 | yes | 0.153 | 0.144 | 0.000148 | 0.000148 | 0.537 | 0.701 |
| All | FH | v_on | 10 min | 0.758 | 0.745 to 0.772 | under-covers | no | 0.766 | yes | 0.129 | 0.113 | 0.000166 | 0.000165 | 0.601 | 0.759 |
| All | FH | v_on | 20 min | 0.826 | 0.814 to 0.837 | under-covers | no | 0.829 | yes | 0.091 | 0.083 | 0.000191 | 0.00019 | 0.691 | 0.826 |
| All | FH | v_on | 30 min | 0.859 | 0.848 to 0.870 | under-covers | no | 0.869 | yes | 0.074 | 0.066 | 0.00021 | 0.000209 | 0.759 | 0.859 |
| All | FH | v_on | 60 min | 0.915 | 0.906 to 0.923 | under-covers | no | 0.923 | yes | 0.048 | 0.037 | 0.000245 | 0.000245 | 0.888 | 0.915 |
| All | FH | v_on | 180 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.958 | no | 0.034 | 0.022 | 0.000276 | 0.000275 | 1.003 | 0.946 |
| All | FS | ips_ratio | rows | 0.909 | 0.899 to 0.917 | under-covers | no | 0.911 | yes | 0.049 | 0.043 | 0.127 | 0.127 | 0.861 | 0.908 |
| All | FS | ips_ratio | impressions | 0.914 | 0.905 to 0.922 | under-covers | no | 0.916 | yes | 0.045 | 0.041 | 0.129 | 0.129 | 0.874 | 0.914 |
| All | FS | ips_ratio | 5 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.954 | yes | 0.025 | 0.024 | 0.149 | 0.149 | 1.008 | 0.952 |
| All | FS | ips_ratio | 10 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.955 | yes | 0.024 | 0.024 | 0.15 | 0.15 | 1.014 | 0.952 |
| All | FS | ips_ratio | 20 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.958 | no | 0.025 | 0.024 | 0.151 | 0.151 | 1.026 | 0.952 |
| All | FS | ips_ratio | 30 min | 0.956 | 0.949 to 0.961 | adequate | yes | 0.960 | yes | 0.021 | 0.023 | 0.153 | 0.153 | 1.038 | 0.956 |
| All | FS | ips_ratio | 60 min | 0.962 | 0.956 to 0.968 | adequate | no | 0.966 | yes | 0.019 | 0.019 | 0.158 | 0.157 | 1.067 | 0.962 |
| All | FS | ips_ratio | 180 min | 0.969 | 0.963 to 0.974 | adequate | no | 0.977 | no | 0.015 | 0.017 | 0.167 | 0.166 | 1.135 | 0.969 |
| All | FS | snips_ratio | rows | 0.907 | 0.897 to 0.915 | under-covers | no | 0.911 | yes | 0.050 | 0.043 | 0.127 | 0.127 | 0.859 | 0.906 |
| All | FS | snips_ratio | impressions | 0.913 | 0.904 to 0.922 | under-covers | no | 0.915 | yes | 0.045 | 0.041 | 0.129 | 0.128 | 0.872 | 0.913 |
| All | FS | snips_ratio | 5 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.951 | yes | 0.025 | 0.027 | 0.147 | 0.146 | 0.994 | 0.947 |
| All | FS | snips_ratio | 10 min | 0.949 | 0.942 to 0.955 | adequate | yes | 0.952 | yes | 0.026 | 0.025 | 0.148 | 0.147 | 1.000 | 0.949 |
| All | FS | snips_ratio | 20 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.955 | yes | 0.025 | 0.025 | 0.149 | 0.149 | 1.012 | 0.950 |
| All | FS | snips_ratio | 30 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.957 | yes | 0.022 | 0.024 | 0.151 | 0.15 | 1.022 | 0.955 |
| All | FS | snips_ratio | 60 min | 0.959 | 0.953 to 0.965 | adequate | no | 0.963 | yes | 0.019 | 0.021 | 0.155 | 0.155 | 1.051 | 0.959 |
| All | FS | snips_ratio | 180 min | 0.968 | 0.962 to 0.973 | adequate | no | 0.976 | no | 0.015 | 0.017 | 0.166 | 0.165 | 1.126 | 0.968 |
| All | FS | ips | rows | 0.917 | 0.908 to 0.925 | under-covers | no | 0.915 | yes | 0.043 | 0.041 | 0.000625 | 0.000624 | 0.875 | 0.917 |
| All | FS | ips | impressions | 0.920 | 0.911 to 0.928 | unresolved | no | 0.920 | yes | 0.041 | 0.040 | 0.000633 | 0.000633 | 0.887 | 0.920 |
| All | FS | ips | 5 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.953 | yes | 0.025 | 0.022 | 0.00072 | 0.000719 | 1.008 | 0.954 |
| All | FS | ips | 10 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.953 | yes | 0.025 | 0.024 | 0.00072 | 0.000719 | 1.007 | 0.952 |
| All | FS | ips | 20 min | 0.950 | 0.943 to 0.957 | adequate | yes | 0.954 | yes | 0.026 | 0.023 | 0.000721 | 0.000718 | 1.008 | 0.950 |
| All | FS | ips | 30 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.954 | yes | 0.024 | 0.024 | 0.000721 | 0.000719 | 1.009 | 0.952 |
| All | FS | ips | 60 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.954 | yes | 0.025 | 0.025 | 0.000719 | 0.000717 | 1.006 | 0.950 |
| All | FS | ips | 180 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.028 | 0.026 | 0.00071 | 0.000705 | 0.994 | 0.947 |
| All | FS | v_on | rows | 0.715 | 0.701 to 0.729 | under-covers | no | 0.710 | yes | 0.146 | 0.139 | 7.82e-05 | 7.81e-05 | 0.545 | 0.715 |
| All | FS | v_on | impressions | 0.749 | 0.735 to 0.762 | under-covers | no | 0.747 | yes | 0.128 | 0.123 | 8.45e-05 | 8.45e-05 | 0.589 | 0.749 |
| All | FS | v_on | 5 min | 0.970 | 0.964 to 0.975 | adequate | no | 0.970 | yes | 0.015 | 0.015 | 0.00016 | 0.00016 | 1.112 | 0.970 |
| All | FS | v_on | 10 min | 0.986 | 0.982 to 0.989 | over-covers | no | 0.986 | yes | 0.008 | 0.006 | 0.000182 | 0.000182 | 1.271 | 0.987 |
| All | FS | v_on | 20 min | 0.997 | 0.995 to 0.998 | over-covers | no | 0.996 | yes | 0.002 | 0.001 | 0.000215 | 0.000214 | 1.497 | 0.997 |
| All | FS | v_on | 30 min | 0.999 | 0.997 to 1.000 | over-covers | no | 0.999 | yes | 0.001 | 0.000 | 0.000239 | 0.000239 | 1.680 | 0.999 |
| All | FS | v_on | 60 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000305 | 0.000305 | 2.125 | 1.000 |
| All | FS | v_on | 180 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000435 | 0.000435 | 3.065 | 1.000 |
| All | S | ips_ratio | rows | 0.952 | 0.944 to 0.958 | adequate | yes | 0.951 | yes | 0.028 | 0.020 | 0.127 | 0.127 | 1.001 | 0.953 |
| All | S | ips_ratio | impressions | 0.952 | 0.944 to 0.958 | adequate | yes | 0.951 | yes | 0.029 | 0.020 | 0.127 | 0.127 | 1.002 | 0.952 |
| All | S | ips_ratio | 5 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.956 | yes | 0.027 | 0.019 | 0.13 | 0.13 | 1.026 | 0.955 |
| All | S | ips_ratio | 10 min | 0.956 | 0.949 to 0.962 | adequate | yes | 0.957 | yes | 0.025 | 0.019 | 0.13 | 0.13 | 1.029 | 0.957 |
| All | S | ips_ratio | 20 min | 0.959 | 0.953 to 0.965 | adequate | no | 0.959 | yes | 0.024 | 0.017 | 0.132 | 0.132 | 1.041 | 0.959 |
| All | S | ips_ratio | 30 min | 0.960 | 0.953 to 0.965 | adequate | no | 0.962 | yes | 0.022 | 0.018 | 0.134 | 0.133 | 1.054 | 0.960 |
| All | S | ips_ratio | 60 min | 0.963 | 0.957 to 0.969 | adequate | no | 0.967 | yes | 0.021 | 0.016 | 0.137 | 0.137 | 1.083 | 0.965 |
| All | S | ips_ratio | 180 min | 0.973 | 0.968 to 0.978 | unresolved | no | 0.978 | no | 0.015 | 0.013 | 0.146 | 0.146 | 1.154 | 0.973 |
| All | S | snips_ratio | rows | 0.951 | 0.943 to 0.957 | adequate | yes | 0.950 | yes | 0.030 | 0.020 | 0.127 | 0.126 | 0.999 | 0.953 |
| All | S | snips_ratio | impressions | 0.952 | 0.945 to 0.958 | adequate | yes | 0.950 | yes | 0.029 | 0.019 | 0.127 | 0.127 | 0.999 | 0.952 |
| All | S | snips_ratio | 5 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.952 | yes | 0.028 | 0.020 | 0.128 | 0.127 | 1.006 | 0.952 |
| All | S | snips_ratio | 10 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.953 | yes | 0.028 | 0.020 | 0.128 | 0.128 | 1.010 | 0.952 |
| All | S | snips_ratio | 20 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.955 | yes | 0.026 | 0.020 | 0.13 | 0.129 | 1.022 | 0.956 |
| All | S | snips_ratio | 30 min | 0.958 | 0.952 to 0.964 | adequate | no | 0.958 | yes | 0.024 | 0.018 | 0.131 | 0.131 | 1.032 | 0.958 |
| All | S | snips_ratio | 60 min | 0.961 | 0.955 to 0.967 | adequate | no | 0.964 | yes | 0.022 | 0.017 | 0.135 | 0.134 | 1.061 | 0.962 |
| All | S | snips_ratio | 180 min | 0.971 | 0.966 to 0.976 | unresolved | no | 0.976 | no | 0.016 | 0.013 | 0.145 | 0.144 | 1.142 | 0.972 |
| All | S | ips | rows | 0.951 | 0.943 to 0.957 | adequate | yes | 0.951 | yes | 0.030 | 0.019 | 0.000624 | 0.000624 | 1.001 | 0.951 |
| All | S | ips | impressions | 0.953 | 0.946 to 0.959 | adequate | yes | 0.951 | yes | 0.029 | 0.018 | 0.000625 | 0.000624 | 1.002 | 0.952 |
| All | S | ips | 5 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.954 | yes | 0.027 | 0.019 | 0.000636 | 0.000635 | 1.019 | 0.955 |
| All | S | ips | 10 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.955 | yes | 0.028 | 0.019 | 0.000634 | 0.000633 | 1.017 | 0.954 |
| All | S | ips | 20 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.955 | yes | 0.027 | 0.019 | 0.000635 | 0.000634 | 1.018 | 0.954 |
| All | S | ips | 30 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.955 | yes | 0.028 | 0.019 | 0.000636 | 0.000635 | 1.019 | 0.954 |
| All | S | ips | 60 min | 0.951 | 0.944 to 0.958 | adequate | yes | 0.955 | yes | 0.029 | 0.020 | 0.000633 | 0.000632 | 1.015 | 0.951 |
| All | S | ips | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.954 | no | 0.030 | 0.022 | 0.000627 | 0.000623 | 1.005 | 0.947 |
| All | S | v_on | rows | 0.945 | 0.938 to 0.952 | adequate | yes | 0.950 | yes | 0.026 | 0.028 | 7.81e-05 | 7.81e-05 | 0.985 | 0.945 |
| All | S | v_on | impressions | 0.943 | 0.935 to 0.949 | adequate | no | 0.950 | no | 0.027 | 0.030 | 7.81e-05 | 7.81e-05 | 0.986 | 0.943 |
| All | S | v_on | 5 min | 0.989 | 0.986 to 0.992 | over-covers | no | 0.992 | no | 0.006 | 0.004 | 0.000105 | 0.000105 | 1.327 | 0.989 |
| All | S | v_on | 10 min | 0.997 | 0.995 to 0.998 | over-covers | no | 0.999 | no | 0.002 | 0.002 | 0.000127 | 0.000127 | 1.617 | 0.997 |
| All | S | v_on | 20 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000161 | 0.000161 | 2.037 | 1.000 |
| All | S | v_on | 30 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000185 | 0.000185 | 2.367 | 1.000 |
| All | S | v_on | 60 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.00025 | 0.00025 | 3.147 | 1.000 |
| All | S | v_on | 180 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000371 | 0.000371 | 4.735 | 1.000 |
| All | M.half-sessions | ips_ratio | rows | 0.884 | 0.874 to 0.894 | under-covers | no | 0.888 | yes | 0.059 | 0.057 | 0.127 | 0.127 | 0.806 | 0.884 |
| All | M.half-sessions | ips_ratio | impressions | 0.902 | 0.892 to 0.911 | under-covers | no | 0.903 | yes | 0.050 | 0.048 | 0.133 | 0.133 | 0.842 | 0.901 |
| All | M.half-sessions | ips_ratio | 5 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.951 | yes | 0.031 | 0.022 | 0.157 | 0.157 | 0.995 | 0.947 |
| All | M.half-sessions | ips_ratio | 10 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.952 | yes | 0.029 | 0.024 | 0.158 | 0.157 | 0.999 | 0.947 |
| All | M.half-sessions | ips_ratio | 20 min | 0.948 | 0.941 to 0.955 | adequate | yes | 0.953 | yes | 0.028 | 0.024 | 0.158 | 0.158 | 1.002 | 0.949 |
| All | M.half-sessions | ips_ratio | 30 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.953 | yes | 0.028 | 0.025 | 0.159 | 0.158 | 1.004 | 0.948 |
| All | M.half-sessions | ips_ratio | 60 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.953 | yes | 0.029 | 0.022 | 0.158 | 0.158 | 1.003 | 0.950 |
| All | M.half-sessions | ips_ratio | 180 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.954 | no | 0.030 | 0.025 | 0.158 | 0.157 | 1.000 | 0.946 |
| All | M.half-sessions | snips_ratio | rows | 0.884 | 0.874 to 0.894 | under-covers | no | 0.887 | yes | 0.059 | 0.057 | 0.127 | 0.127 | 0.804 | 0.884 |
| All | M.half-sessions | snips_ratio | impressions | 0.901 | 0.891 to 0.910 | under-covers | no | 0.903 | yes | 0.051 | 0.049 | 0.133 | 0.133 | 0.840 | 0.901 |
| All | M.half-sessions | snips_ratio | 5 min | 0.942 | 0.934 to 0.949 | adequate | no | 0.948 | yes | 0.033 | 0.025 | 0.155 | 0.155 | 0.983 | 0.943 |
| All | M.half-sessions | snips_ratio | 10 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.949 | yes | 0.030 | 0.025 | 0.156 | 0.155 | 0.986 | 0.945 |
| All | M.half-sessions | snips_ratio | 20 min | 0.945 | 0.938 to 0.952 | adequate | yes | 0.950 | yes | 0.029 | 0.026 | 0.156 | 0.156 | 0.989 | 0.946 |
| All | M.half-sessions | snips_ratio | 30 min | 0.945 | 0.938 to 0.952 | adequate | yes | 0.950 | yes | 0.029 | 0.025 | 0.156 | 0.156 | 0.990 | 0.946 |
| All | M.half-sessions | snips_ratio | 60 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.951 | yes | 0.030 | 0.024 | 0.156 | 0.156 | 0.989 | 0.947 |
| All | M.half-sessions | snips_ratio | 180 min | 0.941 | 0.933 to 0.947 | adequate | no | 0.952 | no | 0.033 | 0.026 | 0.156 | 0.155 | 0.989 | 0.941 |
| All | M.half-sessions | ips | rows | 0.890 | 0.880 to 0.899 | under-covers | no | 0.893 | yes | 0.055 | 0.055 | 0.000626 | 0.000626 | 0.817 | 0.889 |
| All | M.half-sessions | ips | impressions | 0.909 | 0.900 to 0.918 | under-covers | no | 0.906 | yes | 0.046 | 0.044 | 0.000652 | 0.000652 | 0.851 | 0.909 |
| All | M.half-sessions | ips | 5 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.951 | yes | 0.028 | 0.022 | 0.000765 | 0.000763 | 0.998 | 0.951 |
| All | M.half-sessions | ips | 10 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.952 | yes | 0.028 | 0.022 | 0.000766 | 0.000765 | 1.000 | 0.949 |
| All | M.half-sessions | ips | 20 min | 0.951 | 0.944 to 0.958 | adequate | yes | 0.953 | yes | 0.029 | 0.020 | 0.000768 | 0.000766 | 1.002 | 0.951 |
| All | M.half-sessions | ips | 30 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.953 | yes | 0.027 | 0.021 | 0.00077 | 0.000767 | 1.004 | 0.951 |
| All | M.half-sessions | ips | 60 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.953 | yes | 0.027 | 0.022 | 0.000768 | 0.000765 | 1.002 | 0.952 |
| All | M.half-sessions | ips | 180 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.030 | 0.024 | 0.000761 | 0.000759 | 0.994 | 0.945 |
| All | M.half-sessions | v_on | rows | 0.660 | 0.645 to 0.675 | under-covers | no | 0.669 | yes | 0.169 | 0.171 | 7.81e-05 | 7.82e-05 | 0.491 | 0.662 |
| All | M.half-sessions | v_on | impressions | 0.782 | 0.769 to 0.794 | under-covers | no | 0.788 | yes | 0.110 | 0.108 | 0.0001 | 0.0001 | 0.630 | 0.781 |
| All | M.half-sessions | v_on | 5 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.943 | yes | 0.031 | 0.029 | 0.000152 | 0.000152 | 0.959 | 0.940 |
| All | M.half-sessions | v_on | 10 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.950 | yes | 0.027 | 0.026 | 0.000157 | 0.000157 | 0.987 | 0.946 |
| All | M.half-sessions | v_on | 20 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.955 | yes | 0.025 | 0.023 | 0.000161 | 0.000161 | 1.014 | 0.952 |
| All | M.half-sessions | v_on | 30 min | 0.956 | 0.949 to 0.961 | adequate | yes | 0.959 | yes | 0.023 | 0.022 | 0.000164 | 0.000164 | 1.030 | 0.955 |
| All | M.half-sessions | v_on | 60 min | 0.964 | 0.958 to 0.969 | adequate | no | 0.968 | yes | 0.018 | 0.018 | 0.000171 | 0.000171 | 1.074 | 0.964 |
| All | M.half-sessions | v_on | 180 min | 0.975 | 0.970 to 0.980 | unresolved | no | 0.983 | no | 0.015 | 0.010 | 0.000188 | 0.000187 | 1.183 | 0.975 |
| All | M.double-sessions | ips_ratio | rows | 0.863 | 0.852 to 0.873 | under-covers | no | 0.863 | yes | 0.070 | 0.067 | 0.127 | 0.127 | 0.759 | 0.863 |
| All | M.double-sessions | ips_ratio | impressions | 0.877 | 0.867 to 0.887 | under-covers | no | 0.880 | yes | 0.062 | 0.060 | 0.133 | 0.133 | 0.794 | 0.876 |
| All | M.double-sessions | ips_ratio | 5 min | 0.945 | 0.938 to 0.952 | adequate | yes | 0.947 | yes | 0.029 | 0.026 | 0.165 | 0.165 | 0.985 | 0.946 |
| All | M.double-sessions | ips_ratio | 10 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.949 | yes | 0.029 | 0.025 | 0.166 | 0.166 | 0.993 | 0.946 |
| All | M.double-sessions | ips_ratio | 20 min | 0.950 | 0.942 to 0.956 | adequate | yes | 0.951 | yes | 0.028 | 0.022 | 0.168 | 0.168 | 1.002 | 0.949 |
| All | M.double-sessions | ips_ratio | 30 min | 0.949 | 0.942 to 0.955 | adequate | yes | 0.952 | yes | 0.026 | 0.025 | 0.168 | 0.168 | 1.005 | 0.948 |
| All | M.double-sessions | ips_ratio | 60 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.953 | yes | 0.029 | 0.024 | 0.168 | 0.168 | 1.005 | 0.948 |
| All | M.double-sessions | ips_ratio | 180 min | 0.945 | 0.937 to 0.952 | adequate | yes | 0.954 | no | 0.029 | 0.026 | 0.167 | 0.167 | 1.000 | 0.946 |
| All | M.double-sessions | snips_ratio | rows | 0.861 | 0.850 to 0.871 | under-covers | no | 0.863 | yes | 0.071 | 0.068 | 0.127 | 0.127 | 0.757 | 0.861 |
| All | M.double-sessions | snips_ratio | impressions | 0.875 | 0.865 to 0.885 | under-covers | no | 0.880 | yes | 0.064 | 0.061 | 0.133 | 0.133 | 0.792 | 0.876 |
| All | M.double-sessions | snips_ratio | 5 min | 0.943 | 0.936 to 0.950 | adequate | yes | 0.944 | yes | 0.030 | 0.027 | 0.163 | 0.163 | 0.974 | 0.943 |
| All | M.double-sessions | snips_ratio | 10 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.947 | yes | 0.030 | 0.026 | 0.165 | 0.164 | 0.982 | 0.943 |
| All | M.double-sessions | snips_ratio | 20 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.949 | yes | 0.028 | 0.025 | 0.166 | 0.166 | 0.990 | 0.947 |
| All | M.double-sessions | snips_ratio | 30 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.949 | yes | 0.028 | 0.026 | 0.166 | 0.166 | 0.992 | 0.945 |
| All | M.double-sessions | snips_ratio | 60 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.950 | yes | 0.029 | 0.024 | 0.166 | 0.166 | 0.993 | 0.946 |
| All | M.double-sessions | snips_ratio | 180 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.952 | no | 0.030 | 0.027 | 0.166 | 0.165 | 0.991 | 0.943 |
| All | M.double-sessions | ips | rows | 0.867 | 0.856 to 0.877 | under-covers | no | 0.869 | yes | 0.069 | 0.065 | 0.000625 | 0.000625 | 0.771 | 0.867 |
| All | M.double-sessions | ips | impressions | 0.883 | 0.873 to 0.893 | under-covers | no | 0.884 | yes | 0.061 | 0.056 | 0.000651 | 0.000651 | 0.804 | 0.883 |
| All | M.double-sessions | ips | 5 min | 0.949 | 0.941 to 0.955 | adequate | yes | 0.947 | yes | 0.028 | 0.024 | 0.000802 | 0.000801 | 0.989 | 0.948 |
| All | M.double-sessions | ips | 10 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.949 | yes | 0.027 | 0.023 | 0.000808 | 0.000806 | 0.997 | 0.951 |
| All | M.double-sessions | ips | 20 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.951 | yes | 0.025 | 0.022 | 0.000814 | 0.000813 | 1.004 | 0.953 |
| All | M.double-sessions | ips | 30 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.952 | yes | 0.026 | 0.021 | 0.000816 | 0.000815 | 1.007 | 0.953 |
| All | M.double-sessions | ips | 60 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.952 | yes | 0.027 | 0.021 | 0.000815 | 0.000813 | 1.005 | 0.952 |
| All | M.double-sessions | ips | 180 min | 0.945 | 0.937 to 0.952 | adequate | yes | 0.952 | no | 0.031 | 0.024 | 0.000808 | 0.000803 | 0.997 | 0.945 |
| All | M.double-sessions | v_on | rows | 0.639 | 0.624 to 0.654 | under-covers | no | 0.636 | yes | 0.183 | 0.178 | 7.81e-05 | 7.81e-05 | 0.461 | 0.638 |
| All | M.double-sessions | v_on | impressions | 0.762 | 0.749 to 0.775 | under-covers | no | 0.756 | yes | 0.124 | 0.113 | 0.0001 | 0.0001 | 0.591 | 0.762 |
| All | M.double-sessions | v_on | 5 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.941 | yes | 0.033 | 0.030 | 0.000163 | 0.000162 | 0.959 | 0.938 |
| All | M.double-sessions | v_on | 10 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.949 | yes | 0.030 | 0.026 | 0.000167 | 0.000167 | 0.988 | 0.944 |
| All | M.double-sessions | v_on | 20 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.954 | yes | 0.028 | 0.024 | 0.000171 | 0.000171 | 1.012 | 0.948 |
| All | M.double-sessions | v_on | 30 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.958 | no | 0.028 | 0.025 | 0.000174 | 0.000174 | 1.027 | 0.948 |
| All | M.double-sessions | v_on | 60 min | 0.956 | 0.949 to 0.962 | adequate | yes | 0.966 | no | 0.024 | 0.020 | 0.000181 | 0.00018 | 1.066 | 0.957 |
| All | M.double-sessions | v_on | 180 min | 0.970 | 0.964 to 0.975 | adequate | no | 0.981 | no | 0.019 | 0.011 | 0.000197 | 0.000196 | 1.160 | 0.969 |
| All | M.two-level | ips_ratio | rows | 0.873 | 0.862 to 0.883 | under-covers | no | 0.862 | no | 0.067 | 0.060 | 0.127 | 0.127 | 0.769 | 0.873 |
| All | M.two-level | ips_ratio | impressions | 0.886 | 0.876 to 0.896 | under-covers | no | 0.879 | yes | 0.061 | 0.053 | 0.133 | 0.133 | 0.804 | 0.886 |
| All | M.two-level | ips_ratio | 5 min | 0.950 | 0.942 to 0.956 | adequate | yes | 0.949 | yes | 0.027 | 0.023 | 0.167 | 0.167 | 1.012 | 0.950 |
| All | M.two-level | ips_ratio | 10 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.951 | yes | 0.026 | 0.023 | 0.168 | 0.168 | 1.018 | 0.950 |
| All | M.two-level | ips_ratio | 20 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.952 | yes | 0.027 | 0.022 | 0.169 | 0.168 | 1.023 | 0.952 |
| All | M.two-level | ips_ratio | 30 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.952 | yes | 0.025 | 0.021 | 0.169 | 0.169 | 1.025 | 0.953 |
| All | M.two-level | ips_ratio | 60 min | 0.949 | 0.941 to 0.955 | adequate | yes | 0.953 | yes | 0.027 | 0.024 | 0.169 | 0.169 | 1.024 | 0.949 |
| All | M.two-level | ips_ratio | 180 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.954 | yes | 0.029 | 0.024 | 0.168 | 0.168 | 1.019 | 0.947 |
| All | M.two-level | snips_ratio | rows | 0.873 | 0.862 to 0.883 | under-covers | no | 0.861 | no | 0.067 | 0.060 | 0.127 | 0.127 | 0.767 | 0.872 |
| All | M.two-level | snips_ratio | impressions | 0.885 | 0.874 to 0.894 | under-covers | no | 0.878 | yes | 0.061 | 0.054 | 0.132 | 0.132 | 0.802 | 0.886 |
| All | M.two-level | snips_ratio | 5 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.946 | yes | 0.029 | 0.025 | 0.165 | 0.165 | 1.001 | 0.947 |
| All | M.two-level | snips_ratio | 10 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.948 | yes | 0.028 | 0.024 | 0.166 | 0.166 | 1.006 | 0.948 |
| All | M.two-level | snips_ratio | 20 min | 0.948 | 0.941 to 0.955 | adequate | yes | 0.949 | yes | 0.029 | 0.023 | 0.167 | 0.166 | 1.012 | 0.948 |
| All | M.two-level | snips_ratio | 30 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.950 | yes | 0.027 | 0.023 | 0.167 | 0.167 | 1.012 | 0.950 |
| All | M.two-level | snips_ratio | 60 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.950 | yes | 0.028 | 0.025 | 0.167 | 0.167 | 1.012 | 0.948 |
| All | M.two-level | snips_ratio | 180 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.952 | yes | 0.029 | 0.024 | 0.167 | 0.166 | 1.010 | 0.946 |
| All | M.two-level | ips | rows | 0.875 | 0.865 to 0.885 | under-covers | no | 0.867 | yes | 0.068 | 0.057 | 0.000625 | 0.000625 | 0.781 | 0.875 |
| All | M.two-level | ips | impressions | 0.890 | 0.880 to 0.900 | under-covers | no | 0.882 | yes | 0.062 | 0.048 | 0.000651 | 0.00065 | 0.813 | 0.891 |
| All | M.two-level | ips | 5 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.949 | yes | 0.028 | 0.020 | 0.000813 | 0.00081 | 1.016 | 0.952 |
| All | M.two-level | ips | 10 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.951 | yes | 0.027 | 0.021 | 0.000816 | 0.000814 | 1.020 | 0.952 |
| All | M.two-level | ips | 20 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.952 | yes | 0.029 | 0.020 | 0.00082 | 0.000817 | 1.025 | 0.951 |
| All | M.two-level | ips | 30 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.952 | yes | 0.027 | 0.019 | 0.000822 | 0.000819 | 1.026 | 0.954 |
| All | M.two-level | ips | 60 min | 0.953 | 0.945 to 0.959 | adequate | yes | 0.952 | yes | 0.028 | 0.019 | 0.00082 | 0.000816 | 1.024 | 0.953 |
| All | M.two-level | ips | 180 min | 0.951 | 0.943 to 0.957 | adequate | yes | 0.952 | yes | 0.030 | 0.020 | 0.000812 | 0.000806 | 1.014 | 0.951 |
| All | M.two-level | v_on | rows | 0.636 | 0.621 to 0.651 | under-covers | no | 0.637 | yes | 0.190 | 0.174 | 7.81e-05 | 7.81e-05 | 0.462 | 0.634 |
| All | M.two-level | v_on | impressions | 0.747 | 0.733 to 0.760 | under-covers | no | 0.756 | yes | 0.135 | 0.118 | 0.0001 | 0.0001 | 0.592 | 0.748 |
| All | M.two-level | v_on | 5 min | 0.942 | 0.934 to 0.948 | adequate | no | 0.941 | yes | 0.031 | 0.028 | 0.000162 | 0.000162 | 0.960 | 0.943 |
| All | M.two-level | v_on | 10 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.949 | yes | 0.027 | 0.025 | 0.000167 | 0.000167 | 0.989 | 0.948 |
| All | M.two-level | v_on | 20 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.954 | yes | 0.025 | 0.022 | 0.000171 | 0.000171 | 1.013 | 0.953 |
| All | M.two-level | v_on | 30 min | 0.956 | 0.949 to 0.962 | adequate | yes | 0.958 | yes | 0.022 | 0.022 | 0.000174 | 0.000174 | 1.029 | 0.956 |
| All | M.two-level | v_on | 60 min | 0.964 | 0.958 to 0.969 | adequate | no | 0.966 | yes | 0.019 | 0.017 | 0.000181 | 0.000181 | 1.070 | 0.964 |
| All | M.two-level | v_on | 180 min | 0.976 | 0.970 to 0.980 | unresolved | no | 0.981 | no | 0.015 | 0.010 | 0.000197 | 0.000196 | 1.165 | 0.974 |
| All | H.half-long | ips_ratio | rows | 0.799 | 0.787 to 0.811 | under-covers | no | 0.798 | yes | 0.106 | 0.095 | 0.127 | 0.127 | 0.653 | 0.799 |
| All | H.half-long | ips_ratio | impressions | 0.821 | 0.809 to 0.832 | under-covers | no | 0.818 | yes | 0.095 | 0.084 | 0.133 | 0.133 | 0.683 | 0.821 |
| All | H.half-long | ips_ratio | 5 min | 0.912 | 0.903 to 0.920 | under-covers | no | 0.911 | yes | 0.047 | 0.041 | 0.169 | 0.169 | 0.871 | 0.910 |
| All | H.half-long | ips_ratio | 10 min | 0.915 | 0.906 to 0.924 | under-covers | no | 0.918 | yes | 0.045 | 0.040 | 0.173 | 0.172 | 0.886 | 0.915 |
| All | H.half-long | ips_ratio | 20 min | 0.921 | 0.912 to 0.929 | unresolved | no | 0.926 | yes | 0.040 | 0.039 | 0.177 | 0.177 | 0.912 | 0.921 |
| All | H.half-long | ips_ratio | 30 min | 0.929 | 0.921 to 0.937 | unresolved | no | 0.932 | yes | 0.037 | 0.034 | 0.181 | 0.18 | 0.930 | 0.928 |
| All | H.half-long | ips_ratio | 60 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.942 | yes | 0.034 | 0.027 | 0.187 | 0.187 | 0.963 | 0.940 |
| All | H.half-long | ips_ratio | 180 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.949 | no | 0.032 | 0.028 | 0.191 | 0.19 | 0.984 | 0.941 |
| All | H.half-long | snips_ratio | rows | 0.797 | 0.785 to 0.809 | under-covers | no | 0.797 | yes | 0.107 | 0.096 | 0.127 | 0.127 | 0.652 | 0.797 |
| All | H.half-long | snips_ratio | impressions | 0.819 | 0.807 to 0.831 | under-covers | no | 0.817 | yes | 0.096 | 0.085 | 0.133 | 0.132 | 0.682 | 0.820 |
| All | H.half-long | snips_ratio | 5 min | 0.907 | 0.898 to 0.916 | under-covers | no | 0.908 | yes | 0.049 | 0.044 | 0.168 | 0.167 | 0.861 | 0.907 |
| All | H.half-long | snips_ratio | 10 min | 0.913 | 0.904 to 0.921 | under-covers | no | 0.914 | yes | 0.046 | 0.041 | 0.171 | 0.17 | 0.877 | 0.912 |
| All | H.half-long | snips_ratio | 20 min | 0.919 | 0.910 to 0.927 | unresolved | no | 0.923 | yes | 0.041 | 0.040 | 0.175 | 0.175 | 0.902 | 0.919 |
| All | H.half-long | snips_ratio | 30 min | 0.924 | 0.916 to 0.932 | unresolved | no | 0.929 | yes | 0.039 | 0.036 | 0.179 | 0.178 | 0.920 | 0.923 |
| All | H.half-long | snips_ratio | 60 min | 0.936 | 0.928 to 0.943 | adequate | no | 0.940 | yes | 0.035 | 0.029 | 0.186 | 0.185 | 0.954 | 0.936 |
| All | H.half-long | snips_ratio | 180 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.948 | no | 0.034 | 0.028 | 0.19 | 0.189 | 0.976 | 0.939 |
| All | H.half-long | ips | rows | 0.805 | 0.793 to 0.817 | under-covers | no | 0.808 | yes | 0.100 | 0.095 | 0.000625 | 0.000625 | 0.669 | 0.805 |
| All | H.half-long | ips | impressions | 0.823 | 0.811 to 0.834 | under-covers | no | 0.826 | yes | 0.092 | 0.085 | 0.000651 | 0.000651 | 0.697 | 0.824 |
| All | H.half-long | ips | 5 min | 0.911 | 0.902 to 0.920 | under-covers | no | 0.914 | yes | 0.050 | 0.039 | 0.000823 | 0.000822 | 0.881 | 0.912 |
| All | H.half-long | ips | 10 min | 0.920 | 0.911 to 0.928 | unresolved | no | 0.920 | yes | 0.044 | 0.036 | 0.000837 | 0.000835 | 0.896 | 0.920 |
| All | H.half-long | ips | 20 min | 0.924 | 0.916 to 0.932 | unresolved | no | 0.928 | yes | 0.043 | 0.032 | 0.000859 | 0.000857 | 0.919 | 0.924 |
| All | H.half-long | ips | 30 min | 0.929 | 0.921 to 0.937 | unresolved | no | 0.933 | yes | 0.040 | 0.030 | 0.000875 | 0.000871 | 0.936 | 0.928 |
| All | H.half-long | ips | 60 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.942 | yes | 0.037 | 0.026 | 0.000903 | 0.000899 | 0.967 | 0.936 |
| All | H.half-long | ips | 180 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.949 | no | 0.035 | 0.024 | 0.000919 | 0.000916 | 0.983 | 0.941 |
| All | H.half-long | v_on | rows | 0.487 | 0.472 to 0.502 | under-covers | no | 0.489 | yes | 0.255 | 0.259 | 7.82e-05 | 7.82e-05 | 0.338 | 0.486 |
| All | H.half-long | v_on | impressions | 0.605 | 0.590 to 0.620 | under-covers | no | 0.601 | yes | 0.193 | 0.202 | 0.0001 | 0.0001 | 0.433 | 0.605 |
| All | H.half-long | v_on | 5 min | 0.839 | 0.827 to 0.850 | under-covers | no | 0.839 | yes | 0.082 | 0.079 | 0.000167 | 0.000166 | 0.720 | 0.839 |
| All | H.half-long | v_on | 10 min | 0.864 | 0.853 to 0.875 | under-covers | no | 0.865 | yes | 0.070 | 0.066 | 0.000177 | 0.000177 | 0.765 | 0.863 |
| All | H.half-long | v_on | 20 min | 0.894 | 0.884 to 0.903 | under-covers | no | 0.893 | yes | 0.053 | 0.053 | 0.000191 | 0.000191 | 0.825 | 0.893 |
| All | H.half-long | v_on | 30 min | 0.910 | 0.901 to 0.919 | under-covers | no | 0.911 | yes | 0.045 | 0.045 | 0.000201 | 0.000201 | 0.869 | 0.911 |
| All | H.half-long | v_on | 60 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.940 | yes | 0.030 | 0.029 | 0.000222 | 0.000222 | 0.959 | 0.941 |
| All | H.half-long | v_on | 180 min | 0.958 | 0.951 to 0.963 | adequate | no | 0.965 | no | 0.023 | 0.019 | 0.000245 | 0.000244 | 1.060 | 0.959 |
| All | H.double-long | ips_ratio | rows | 0.785 | 0.773 to 0.798 | under-covers | no | 0.794 | yes | 0.107 | 0.107 | 0.127 | 0.127 | 0.637 | 0.785 |
| All | H.double-long | ips_ratio | impressions | 0.807 | 0.795 to 0.819 | under-covers | no | 0.814 | yes | 0.095 | 0.097 | 0.133 | 0.133 | 0.666 | 0.807 |
| All | H.double-long | ips_ratio | 5 min | 0.901 | 0.891 to 0.910 | under-covers | no | 0.908 | yes | 0.055 | 0.044 | 0.169 | 0.169 | 0.850 | 0.903 |
| All | H.double-long | ips_ratio | 10 min | 0.907 | 0.898 to 0.916 | under-covers | no | 0.915 | yes | 0.051 | 0.042 | 0.173 | 0.173 | 0.867 | 0.907 |
| All | H.double-long | ips_ratio | 20 min | 0.917 | 0.909 to 0.926 | unresolved | no | 0.924 | yes | 0.046 | 0.036 | 0.178 | 0.177 | 0.892 | 0.915 |
| All | H.double-long | ips_ratio | 30 min | 0.925 | 0.916 to 0.933 | unresolved | no | 0.930 | yes | 0.042 | 0.033 | 0.181 | 0.181 | 0.910 | 0.924 |
| All | H.double-long | ips_ratio | 60 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.942 | yes | 0.036 | 0.026 | 0.189 | 0.188 | 0.948 | 0.937 |
| All | H.double-long | ips_ratio | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.949 | no | 0.035 | 0.028 | 0.193 | 0.191 | 0.967 | 0.938 |
| All | H.double-long | snips_ratio | rows | 0.785 | 0.773 to 0.798 | under-covers | no | 0.793 | yes | 0.107 | 0.107 | 0.127 | 0.127 | 0.636 | 0.783 |
| All | H.double-long | snips_ratio | impressions | 0.805 | 0.793 to 0.817 | under-covers | no | 0.813 | yes | 0.097 | 0.098 | 0.133 | 0.132 | 0.665 | 0.805 |
| All | H.double-long | snips_ratio | 5 min | 0.900 | 0.890 to 0.909 | under-covers | no | 0.905 | yes | 0.055 | 0.045 | 0.168 | 0.167 | 0.841 | 0.898 |
| All | H.double-long | snips_ratio | 10 min | 0.906 | 0.896 to 0.914 | under-covers | no | 0.912 | yes | 0.051 | 0.043 | 0.171 | 0.171 | 0.858 | 0.905 |
| All | H.double-long | snips_ratio | 20 min | 0.915 | 0.906 to 0.924 | under-covers | no | 0.921 | yes | 0.048 | 0.037 | 0.176 | 0.176 | 0.883 | 0.914 |
| All | H.double-long | snips_ratio | 30 min | 0.921 | 0.912 to 0.929 | unresolved | no | 0.927 | yes | 0.044 | 0.035 | 0.179 | 0.179 | 0.900 | 0.920 |
| All | H.double-long | snips_ratio | 60 min | 0.932 | 0.924 to 0.940 | unresolved | no | 0.939 | yes | 0.038 | 0.029 | 0.187 | 0.187 | 0.939 | 0.935 |
| All | H.double-long | snips_ratio | 180 min | 0.935 | 0.927 to 0.942 | adequate | no | 0.947 | no | 0.035 | 0.030 | 0.191 | 0.189 | 0.959 | 0.935 |
| All | H.double-long | ips | rows | 0.796 | 0.783 to 0.808 | under-covers | no | 0.804 | yes | 0.103 | 0.101 | 0.000625 | 0.000625 | 0.655 | 0.797 |
| All | H.double-long | ips | impressions | 0.816 | 0.803 to 0.827 | under-covers | no | 0.822 | yes | 0.093 | 0.091 | 0.000651 | 0.000651 | 0.682 | 0.815 |
| All | H.double-long | ips | 5 min | 0.911 | 0.902 to 0.920 | under-covers | no | 0.911 | yes | 0.047 | 0.041 | 0.000824 | 0.000822 | 0.863 | 0.910 |
| All | H.double-long | ips | 10 min | 0.916 | 0.907 to 0.924 | under-covers | no | 0.918 | yes | 0.044 | 0.040 | 0.000839 | 0.000837 | 0.878 | 0.916 |
| All | H.double-long | ips | 20 min | 0.922 | 0.914 to 0.930 | unresolved | no | 0.926 | yes | 0.042 | 0.036 | 0.000861 | 0.000858 | 0.901 | 0.921 |
| All | H.double-long | ips | 30 min | 0.927 | 0.919 to 0.935 | unresolved | no | 0.931 | yes | 0.040 | 0.033 | 0.000877 | 0.000874 | 0.918 | 0.929 |
| All | H.double-long | ips | 60 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.942 | yes | 0.033 | 0.026 | 0.000912 | 0.000908 | 0.954 | 0.941 |
| All | H.double-long | ips | 180 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.948 | no | 0.032 | 0.028 | 0.000925 | 0.000919 | 0.969 | 0.940 |
| All | H.double-long | v_on | rows | 0.491 | 0.476 to 0.506 | under-covers | no | 0.481 | yes | 0.255 | 0.254 | 7.81e-05 | 7.82e-05 | 0.326 | 0.491 |
| All | H.double-long | v_on | impressions | 0.594 | 0.578 to 0.609 | under-covers | no | 0.592 | yes | 0.203 | 0.203 | 0.0001 | 0.0001 | 0.417 | 0.593 |
| All | H.double-long | v_on | 5 min | 0.822 | 0.809 to 0.833 | under-covers | no | 0.832 | yes | 0.091 | 0.087 | 0.000167 | 0.000167 | 0.696 | 0.820 |
| All | H.double-long | v_on | 10 min | 0.847 | 0.835 to 0.857 | under-covers | no | 0.859 | no | 0.080 | 0.074 | 0.000178 | 0.000178 | 0.741 | 0.847 |
| All | H.double-long | v_on | 20 min | 0.879 | 0.869 to 0.889 | under-covers | no | 0.889 | yes | 0.062 | 0.058 | 0.000192 | 0.000192 | 0.802 | 0.880 |
| All | H.double-long | v_on | 30 min | 0.898 | 0.888 to 0.907 | under-covers | no | 0.908 | no | 0.051 | 0.051 | 0.000203 | 0.000203 | 0.846 | 0.898 |
| All | H.double-long | v_on | 60 min | 0.927 | 0.918 to 0.934 | unresolved | no | 0.939 | no | 0.039 | 0.034 | 0.000225 | 0.000224 | 0.937 | 0.927 |
| All | H.double-long | v_on | 180 min | 0.950 | 0.943 to 0.957 | adequate | yes | 0.965 | no | 0.030 | 0.019 | 0.000249 | 0.000248 | 1.040 | 0.950 |
| All | H.two-level | ips_ratio | rows | 0.793 | 0.780 to 0.805 | under-covers | no | 0.794 | yes | 0.106 | 0.101 | 0.127 | 0.127 | 0.649 | 0.793 |
| All | H.two-level | ips_ratio | impressions | 0.816 | 0.804 to 0.828 | under-covers | no | 0.814 | yes | 0.096 | 0.088 | 0.133 | 0.133 | 0.678 | 0.816 |
| All | H.two-level | ips_ratio | 5 min | 0.909 | 0.900 to 0.918 | under-covers | no | 0.909 | yes | 0.050 | 0.041 | 0.169 | 0.169 | 0.864 | 0.909 |
| All | H.two-level | ips_ratio | 10 min | 0.914 | 0.905 to 0.923 | under-covers | no | 0.915 | yes | 0.046 | 0.040 | 0.173 | 0.172 | 0.882 | 0.914 |
| All | H.two-level | ips_ratio | 20 min | 0.921 | 0.912 to 0.929 | unresolved | no | 0.924 | yes | 0.043 | 0.036 | 0.178 | 0.177 | 0.907 | 0.921 |
| All | H.two-level | ips_ratio | 30 min | 0.929 | 0.921 to 0.937 | unresolved | no | 0.931 | yes | 0.039 | 0.032 | 0.181 | 0.18 | 0.926 | 0.928 |
| All | H.two-level | ips_ratio | 60 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.942 | yes | 0.036 | 0.026 | 0.189 | 0.187 | 0.962 | 0.938 |
| All | H.two-level | ips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.949 | no | 0.035 | 0.027 | 0.193 | 0.192 | 0.983 | 0.938 |
| All | H.two-level | snips_ratio | rows | 0.792 | 0.780 to 0.805 | under-covers | no | 0.793 | yes | 0.106 | 0.101 | 0.127 | 0.127 | 0.647 | 0.792 |
| All | H.two-level | snips_ratio | impressions | 0.814 | 0.801 to 0.826 | under-covers | no | 0.813 | yes | 0.097 | 0.089 | 0.133 | 0.132 | 0.676 | 0.816 |
| All | H.two-level | snips_ratio | 5 min | 0.906 | 0.897 to 0.915 | under-covers | no | 0.905 | yes | 0.051 | 0.043 | 0.168 | 0.167 | 0.855 | 0.905 |
| All | H.two-level | snips_ratio | 10 min | 0.912 | 0.903 to 0.921 | under-covers | no | 0.912 | yes | 0.048 | 0.040 | 0.171 | 0.17 | 0.872 | 0.911 |
| All | H.two-level | snips_ratio | 20 min | 0.921 | 0.912 to 0.929 | unresolved | no | 0.921 | yes | 0.043 | 0.036 | 0.176 | 0.175 | 0.898 | 0.921 |
| All | H.two-level | snips_ratio | 30 min | 0.926 | 0.917 to 0.933 | unresolved | no | 0.927 | yes | 0.041 | 0.033 | 0.179 | 0.179 | 0.915 | 0.925 |
| All | H.two-level | snips_ratio | 60 min | 0.936 | 0.928 to 0.943 | adequate | no | 0.940 | yes | 0.036 | 0.028 | 0.187 | 0.186 | 0.953 | 0.936 |
| All | H.two-level | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.948 | no | 0.035 | 0.027 | 0.191 | 0.19 | 0.976 | 0.938 |
| All | H.two-level | ips | rows | 0.807 | 0.795 to 0.819 | under-covers | no | 0.804 | yes | 0.100 | 0.093 | 0.000626 | 0.000625 | 0.667 | 0.807 |
| All | H.two-level | ips | impressions | 0.826 | 0.814 to 0.838 | under-covers | no | 0.822 | yes | 0.091 | 0.083 | 0.000651 | 0.00065 | 0.694 | 0.826 |
| All | H.two-level | ips | 5 min | 0.915 | 0.906 to 0.923 | under-covers | no | 0.912 | yes | 0.046 | 0.039 | 0.000823 | 0.000819 | 0.878 | 0.915 |
| All | H.two-level | ips | 10 min | 0.920 | 0.911 to 0.928 | unresolved | no | 0.918 | yes | 0.045 | 0.035 | 0.000838 | 0.000835 | 0.894 | 0.920 |
| All | H.two-level | ips | 20 min | 0.928 | 0.920 to 0.936 | unresolved | no | 0.926 | yes | 0.040 | 0.032 | 0.000861 | 0.000856 | 0.918 | 0.930 |
| All | H.two-level | ips | 30 min | 0.931 | 0.923 to 0.939 | unresolved | no | 0.932 | yes | 0.038 | 0.030 | 0.000877 | 0.000873 | 0.935 | 0.930 |
| All | H.two-level | ips | 60 min | 0.940 | 0.932 to 0.946 | adequate | no | 0.942 | yes | 0.035 | 0.025 | 0.000908 | 0.000902 | 0.969 | 0.940 |
| All | H.two-level | ips | 180 min | 0.942 | 0.934 to 0.948 | adequate | no | 0.949 | no | 0.034 | 0.024 | 0.000923 | 0.000917 | 0.985 | 0.941 |
| All | H.two-level | v_on | rows | 0.482 | 0.467 to 0.498 | under-covers | no | 0.482 | yes | 0.259 | 0.259 | 7.81e-05 | 7.81e-05 | 0.325 | 0.482 |
| All | H.two-level | v_on | impressions | 0.594 | 0.578 to 0.609 | under-covers | no | 0.593 | yes | 0.206 | 0.201 | 0.0001 | 0.0001 | 0.417 | 0.595 |
| All | H.two-level | v_on | 5 min | 0.832 | 0.820 to 0.844 | under-covers | no | 0.833 | yes | 0.087 | 0.081 | 0.000167 | 0.000167 | 0.694 | 0.832 |
| All | H.two-level | v_on | 10 min | 0.858 | 0.847 to 0.869 | under-covers | no | 0.859 | yes | 0.075 | 0.067 | 0.000178 | 0.000178 | 0.740 | 0.859 |
| All | H.two-level | v_on | 20 min | 0.886 | 0.876 to 0.896 | under-covers | no | 0.889 | yes | 0.057 | 0.057 | 0.000192 | 0.000192 | 0.801 | 0.885 |
| All | H.two-level | v_on | 30 min | 0.903 | 0.893 to 0.912 | under-covers | no | 0.908 | yes | 0.050 | 0.048 | 0.000203 | 0.000202 | 0.844 | 0.902 |
| All | H.two-level | v_on | 60 min | 0.931 | 0.922 to 0.938 | unresolved | no | 0.939 | no | 0.035 | 0.034 | 0.000225 | 0.000224 | 0.935 | 0.931 |
| All | H.two-level | v_on | 180 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.965 | no | 0.025 | 0.022 | 0.000248 | 0.000247 | 1.035 | 0.952 |
| Women's | F | ips_ratio | rows | 0.922 | 0.914 to 0.930 | unresolved | no | 0.924 | yes | 0.043 | 0.034 | 0.125 | 0.125 | 0.904 | 0.924 |
| Women's | F | ips_ratio | impressions | 0.928 | 0.920 to 0.936 | unresolved | no | 0.928 | yes | 0.040 | 0.032 | 0.126 | 0.126 | 0.917 | 0.928 |
| Women's | F | ips_ratio | 5 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.952 | yes | 0.027 | 0.021 | 0.139 | 0.139 | 1.006 | 0.952 |
| Women's | F | ips_ratio | 10 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.953 | yes | 0.029 | 0.020 | 0.14 | 0.139 | 1.011 | 0.951 |
| Women's | F | ips_ratio | 20 min | 0.951 | 0.943 to 0.957 | adequate | yes | 0.954 | yes | 0.028 | 0.022 | 0.14 | 0.14 | 1.014 | 0.950 |
| Women's | F | ips_ratio | 30 min | 0.953 | 0.945 to 0.959 | adequate | yes | 0.954 | yes | 0.027 | 0.021 | 0.14 | 0.139 | 1.015 | 0.953 |
| Women's | F | ips_ratio | 60 min | 0.951 | 0.944 to 0.958 | adequate | yes | 0.955 | yes | 0.028 | 0.021 | 0.14 | 0.14 | 1.016 | 0.951 |
| Women's | F | ips_ratio | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.955 | no | 0.030 | 0.022 | 0.139 | 0.139 | 1.010 | 0.947 |
| Women's | F | snips_ratio | rows | 0.922 | 0.914 to 0.930 | unresolved | no | 0.923 | yes | 0.043 | 0.035 | 0.124 | 0.124 | 0.901 | 0.922 |
| Women's | F | snips_ratio | impressions | 0.927 | 0.919 to 0.935 | unresolved | no | 0.927 | yes | 0.041 | 0.032 | 0.126 | 0.126 | 0.915 | 0.926 |
| Women's | F | snips_ratio | 5 min | 0.949 | 0.942 to 0.955 | adequate | yes | 0.948 | yes | 0.028 | 0.023 | 0.137 | 0.137 | 0.991 | 0.949 |
| Women's | F | snips_ratio | 10 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.949 | yes | 0.030 | 0.022 | 0.137 | 0.137 | 0.994 | 0.947 |
| Women's | F | snips_ratio | 20 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.950 | yes | 0.029 | 0.024 | 0.137 | 0.137 | 0.997 | 0.947 |
| Women's | F | snips_ratio | 30 min | 0.949 | 0.941 to 0.955 | adequate | yes | 0.950 | yes | 0.028 | 0.023 | 0.137 | 0.137 | 0.997 | 0.949 |
| Women's | F | snips_ratio | 60 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.950 | yes | 0.030 | 0.024 | 0.137 | 0.137 | 0.996 | 0.946 |
| Women's | F | snips_ratio | 180 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.951 | no | 0.032 | 0.025 | 0.137 | 0.136 | 0.992 | 0.943 |
| Women's | F | ips | rows | 0.930 | 0.922 to 0.938 | unresolved | no | 0.932 | yes | 0.038 | 0.031 | 0.000787 | 0.000786 | 0.938 | 0.930 |
| Women's | F | ips | impressions | 0.936 | 0.928 to 0.943 | adequate | no | 0.936 | yes | 0.036 | 0.028 | 0.000797 | 0.000797 | 0.950 | 0.937 |
| Women's | F | ips | 5 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.953 | yes | 0.027 | 0.018 | 0.000855 | 0.000854 | 1.019 | 0.955 |
| Women's | F | ips | 10 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.954 | yes | 0.028 | 0.020 | 0.000858 | 0.000857 | 1.022 | 0.953 |
| Women's | F | ips | 20 min | 0.953 | 0.945 to 0.959 | adequate | yes | 0.954 | yes | 0.027 | 0.021 | 0.000859 | 0.000857 | 1.024 | 0.952 |
| Women's | F | ips | 30 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.954 | yes | 0.029 | 0.019 | 0.00086 | 0.000858 | 1.025 | 0.951 |
| Women's | F | ips | 60 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.955 | yes | 0.027 | 0.018 | 0.00086 | 0.000859 | 1.026 | 0.954 |
| Women's | F | ips | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.955 | no | 0.031 | 0.022 | 0.000852 | 0.000849 | 1.017 | 0.948 |
| Women's | F | v_on | rows | 0.636 | 0.621 to 0.651 | under-covers | no | 0.639 | yes | 0.182 | 0.182 | 0.000112 | 0.000112 | 0.462 | 0.636 |
| Women's | F | v_on | impressions | 0.667 | 0.652 to 0.681 | under-covers | no | 0.672 | yes | 0.168 | 0.166 | 0.00012 | 0.00012 | 0.494 | 0.666 |
| Women's | F | v_on | 5 min | 0.935 | 0.927 to 0.943 | adequate | no | 0.938 | yes | 0.029 | 0.035 | 0.000228 | 0.000228 | 0.942 | 0.935 |
| Women's | F | v_on | 10 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.946 | yes | 0.026 | 0.031 | 0.000235 | 0.000234 | 0.970 | 0.943 |
| Women's | F | v_on | 20 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.950 | yes | 0.025 | 0.028 | 0.000239 | 0.000239 | 0.987 | 0.947 |
| Women's | F | v_on | 30 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.952 | yes | 0.024 | 0.028 | 0.000241 | 0.00024 | 0.994 | 0.947 |
| Women's | F | v_on | 60 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.956 | yes | 0.024 | 0.025 | 0.000244 | 0.000244 | 1.009 | 0.952 |
| Women's | F | v_on | 180 min | 0.957 | 0.950 to 0.962 | adequate | yes | 0.966 | no | 0.024 | 0.020 | 0.000254 | 0.000253 | 1.051 | 0.957 |
| Women's | FH | ips_ratio | rows | 0.739 | 0.725 to 0.752 | under-covers | no | 0.746 | yes | 0.134 | 0.128 | 0.125 | 0.125 | 0.584 | 0.740 |
| Women's | FH | ips_ratio | impressions | 0.749 | 0.736 to 0.762 | under-covers | no | 0.753 | yes | 0.129 | 0.122 | 0.127 | 0.126 | 0.593 | 0.745 |
| Women's | FH | ips_ratio | 5 min | 0.809 | 0.796 to 0.821 | under-covers | no | 0.815 | yes | 0.100 | 0.091 | 0.144 | 0.144 | 0.677 | 0.808 |
| Women's | FH | ips_ratio | 10 min | 0.830 | 0.818 to 0.841 | under-covers | no | 0.838 | yes | 0.087 | 0.083 | 0.152 | 0.152 | 0.712 | 0.829 |
| Women's | FH | ips_ratio | 20 min | 0.863 | 0.852 to 0.873 | under-covers | no | 0.869 | yes | 0.069 | 0.069 | 0.164 | 0.164 | 0.770 | 0.862 |
| Women's | FH | ips_ratio | 30 min | 0.884 | 0.874 to 0.894 | under-covers | no | 0.892 | yes | 0.059 | 0.057 | 0.175 | 0.174 | 0.818 | 0.884 |
| Women's | FH | ips_ratio | 60 min | 0.917 | 0.908 to 0.925 | unresolved | no | 0.923 | yes | 0.043 | 0.040 | 0.191 | 0.19 | 0.896 | 0.917 |
| Women's | FH | ips_ratio | 180 min | 0.934 | 0.926 to 0.942 | adequate | no | 0.943 | no | 0.032 | 0.033 | 0.204 | 0.203 | 0.957 | 0.935 |
| Women's | FH | snips_ratio | rows | 0.738 | 0.724 to 0.752 | under-covers | no | 0.744 | yes | 0.134 | 0.128 | 0.124 | 0.124 | 0.582 | 0.740 |
| Women's | FH | snips_ratio | impressions | 0.746 | 0.732 to 0.759 | under-covers | no | 0.752 | yes | 0.130 | 0.124 | 0.126 | 0.126 | 0.591 | 0.746 |
| Women's | FH | snips_ratio | 5 min | 0.801 | 0.789 to 0.814 | under-covers | no | 0.809 | yes | 0.103 | 0.096 | 0.142 | 0.142 | 0.668 | 0.802 |
| Women's | FH | snips_ratio | 10 min | 0.824 | 0.811 to 0.835 | under-covers | no | 0.832 | yes | 0.091 | 0.086 | 0.15 | 0.15 | 0.702 | 0.822 |
| Women's | FH | snips_ratio | 20 min | 0.856 | 0.845 to 0.867 | under-covers | no | 0.864 | yes | 0.073 | 0.070 | 0.162 | 0.162 | 0.761 | 0.855 |
| Women's | FH | snips_ratio | 30 min | 0.881 | 0.871 to 0.891 | under-covers | no | 0.888 | yes | 0.061 | 0.058 | 0.173 | 0.172 | 0.809 | 0.880 |
| Women's | FH | snips_ratio | 60 min | 0.914 | 0.905 to 0.922 | under-covers | no | 0.920 | yes | 0.044 | 0.042 | 0.189 | 0.188 | 0.886 | 0.914 |
| Women's | FH | snips_ratio | 180 min | 0.935 | 0.927 to 0.942 | adequate | no | 0.942 | yes | 0.033 | 0.032 | 0.203 | 0.202 | 0.950 | 0.933 |
| Women's | FH | ips | rows | 0.838 | 0.826 to 0.849 | under-covers | no | 0.837 | yes | 0.084 | 0.078 | 0.000786 | 0.000786 | 0.711 | 0.837 |
| Women's | FH | ips | impressions | 0.844 | 0.832 to 0.855 | under-covers | no | 0.843 | yes | 0.080 | 0.076 | 0.000797 | 0.000796 | 0.720 | 0.844 |
| Women's | FH | ips | 5 min | 0.881 | 0.871 to 0.891 | under-covers | no | 0.880 | yes | 0.060 | 0.059 | 0.000874 | 0.000872 | 0.790 | 0.881 |
| Women's | FH | ips | 10 min | 0.892 | 0.883 to 0.902 | under-covers | no | 0.890 | yes | 0.055 | 0.052 | 0.000898 | 0.000895 | 0.811 | 0.892 |
| Women's | FH | ips | 20 min | 0.907 | 0.897 to 0.915 | under-covers | no | 0.905 | yes | 0.047 | 0.046 | 0.000936 | 0.000933 | 0.846 | 0.907 |
| Women's | FH | ips | 30 min | 0.920 | 0.911 to 0.928 | unresolved | no | 0.918 | yes | 0.041 | 0.040 | 0.000973 | 0.00097 | 0.880 | 0.920 |
| Women's | FH | ips | 60 min | 0.931 | 0.923 to 0.938 | unresolved | no | 0.933 | yes | 0.036 | 0.033 | 0.00102 | 0.00102 | 0.926 | 0.931 |
| Women's | FH | ips | 180 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.947 | yes | 0.033 | 0.026 | 0.00107 | 0.00106 | 0.965 | 0.941 |
| Women's | FH | v_on | rows | 0.208 | 0.195 to 0.221 | under-covers | no | 0.215 | yes | 0.403 | 0.389 | 0.000112 | 0.000112 | 0.138 | 0.208 |
| Women's | FH | v_on | impressions | 0.223 | 0.211 to 0.236 | under-covers | no | 0.230 | yes | 0.396 | 0.381 | 0.00012 | 0.00012 | 0.148 | 0.221 |
| Women's | FH | v_on | 5 min | 0.502 | 0.487 to 0.518 | under-covers | no | 0.524 | no | 0.254 | 0.243 | 0.00029 | 0.000289 | 0.358 | 0.503 |
| Women's | FH | v_on | 10 min | 0.603 | 0.588 to 0.618 | under-covers | no | 0.630 | no | 0.205 | 0.192 | 0.000363 | 0.000362 | 0.449 | 0.604 |
| Women's | FH | v_on | 20 min | 0.734 | 0.720 to 0.747 | under-covers | no | 0.751 | no | 0.143 | 0.123 | 0.000467 | 0.000466 | 0.577 | 0.733 |
| Women's | FH | v_on | 30 min | 0.796 | 0.783 to 0.808 | under-covers | no | 0.816 | no | 0.111 | 0.093 | 0.000537 | 0.000535 | 0.663 | 0.796 |
| Women's | FH | v_on | 60 min | 0.888 | 0.878 to 0.897 | under-covers | no | 0.897 | no | 0.062 | 0.050 | 0.000659 | 0.000656 | 0.814 | 0.888 |
| Women's | FH | v_on | 180 min | 0.923 | 0.915 to 0.931 | unresolved | no | 0.937 | no | 0.045 | 0.031 | 0.000742 | 0.000737 | 0.918 | 0.925 |
| Women's | FS | ips_ratio | rows | 0.922 | 0.913 to 0.930 | unresolved | no | 0.923 | yes | 0.043 | 0.035 | 0.125 | 0.125 | 0.903 | 0.922 |
| Women's | FS | ips_ratio | impressions | 0.927 | 0.918 to 0.934 | unresolved | no | 0.927 | yes | 0.040 | 0.034 | 0.126 | 0.126 | 0.917 | 0.927 |
| Women's | FS | ips_ratio | 5 min | 0.956 | 0.949 to 0.962 | adequate | yes | 0.956 | yes | 0.024 | 0.020 | 0.141 | 0.141 | 1.024 | 0.956 |
| Women's | FS | ips_ratio | 10 min | 0.960 | 0.953 to 0.966 | adequate | no | 0.960 | yes | 0.022 | 0.018 | 0.144 | 0.144 | 1.048 | 0.960 |
| Women's | FS | ips_ratio | 20 min | 0.965 | 0.959 to 0.970 | adequate | no | 0.966 | yes | 0.019 | 0.015 | 0.149 | 0.149 | 1.084 | 0.965 |
| Women's | FS | ips_ratio | 30 min | 0.967 | 0.961 to 0.972 | adequate | no | 0.971 | yes | 0.019 | 0.013 | 0.152 | 0.152 | 1.107 | 0.967 |
| Women's | FS | ips_ratio | 60 min | 0.979 | 0.974 to 0.983 | unresolved | no | 0.981 | yes | 0.013 | 0.008 | 0.165 | 0.164 | 1.194 | 0.979 |
| Women's | FS | ips_ratio | 180 min | 0.993 | 0.989 to 0.995 | over-covers | no | 0.995 | no | 0.004 | 0.004 | 0.195 | 0.194 | 1.415 | 0.993 |
| Women's | FS | snips_ratio | rows | 0.922 | 0.913 to 0.930 | unresolved | no | 0.922 | yes | 0.042 | 0.036 | 0.124 | 0.124 | 0.901 | 0.922 |
| Women's | FS | snips_ratio | impressions | 0.926 | 0.918 to 0.934 | unresolved | no | 0.926 | yes | 0.040 | 0.034 | 0.126 | 0.126 | 0.915 | 0.926 |
| Women's | FS | snips_ratio | 5 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.952 | yes | 0.025 | 0.022 | 0.139 | 0.139 | 1.011 | 0.953 |
| Women's | FS | snips_ratio | 10 min | 0.956 | 0.949 to 0.962 | adequate | yes | 0.957 | yes | 0.024 | 0.020 | 0.142 | 0.142 | 1.030 | 0.956 |
| Women's | FS | snips_ratio | 20 min | 0.963 | 0.956 to 0.968 | adequate | no | 0.963 | yes | 0.021 | 0.016 | 0.147 | 0.147 | 1.067 | 0.962 |
| Women's | FS | snips_ratio | 30 min | 0.966 | 0.960 to 0.971 | adequate | no | 0.968 | yes | 0.019 | 0.015 | 0.15 | 0.15 | 1.092 | 0.966 |
| Women's | FS | snips_ratio | 60 min | 0.976 | 0.971 to 0.981 | unresolved | no | 0.979 | yes | 0.014 | 0.010 | 0.162 | 0.162 | 1.176 | 0.976 |
| Women's | FS | snips_ratio | 180 min | 0.992 | 0.988 to 0.994 | over-covers | no | 0.994 | no | 0.003 | 0.005 | 0.192 | 0.191 | 1.394 | 0.991 |
| Women's | FS | ips | rows | 0.927 | 0.918 to 0.934 | unresolved | no | 0.932 | yes | 0.040 | 0.034 | 0.000786 | 0.000786 | 0.929 | 0.927 |
| Women's | FS | ips | impressions | 0.929 | 0.921 to 0.937 | unresolved | no | 0.936 | yes | 0.038 | 0.033 | 0.000797 | 0.000796 | 0.942 | 0.930 |
| Women's | FS | ips | 5 min | 0.949 | 0.941 to 0.955 | adequate | yes | 0.953 | yes | 0.029 | 0.022 | 0.000854 | 0.000853 | 1.010 | 0.949 |
| Women's | FS | ips | 10 min | 0.949 | 0.942 to 0.955 | adequate | yes | 0.954 | yes | 0.028 | 0.023 | 0.000856 | 0.000855 | 1.013 | 0.949 |
| Women's | FS | ips | 20 min | 0.949 | 0.941 to 0.955 | adequate | yes | 0.954 | yes | 0.028 | 0.023 | 0.000857 | 0.000856 | 1.014 | 0.948 |
| Women's | FS | ips | 30 min | 0.949 | 0.941 to 0.955 | adequate | yes | 0.954 | yes | 0.029 | 0.022 | 0.000857 | 0.000856 | 1.014 | 0.949 |
| Women's | FS | ips | 60 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.955 | yes | 0.029 | 0.021 | 0.000859 | 0.000856 | 1.016 | 0.951 |
| Women's | FS | ips | 180 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.955 | no | 0.032 | 0.025 | 0.000852 | 0.000847 | 1.007 | 0.943 |
| Women's | FS | v_on | rows | 0.613 | 0.598 to 0.628 | under-covers | no | 0.623 | yes | 0.195 | 0.192 | 0.000112 | 0.000112 | 0.445 | 0.614 |
| Women's | FS | v_on | impressions | 0.651 | 0.636 to 0.665 | under-covers | no | 0.659 | yes | 0.176 | 0.173 | 0.00012 | 0.00012 | 0.480 | 0.650 |
| Women's | FS | v_on | 5 min | 0.971 | 0.966 to 0.976 | unresolved | no | 0.976 | no | 0.015 | 0.014 | 0.000285 | 0.000285 | 1.136 | 0.972 |
| Women's | FS | v_on | 10 min | 0.989 | 0.986 to 0.992 | over-covers | no | 0.992 | yes | 0.006 | 0.005 | 0.000332 | 0.000332 | 1.324 | 0.989 |
| Women's | FS | v_on | 20 min | 0.999 | 0.997 to 0.999 | over-covers | no | 0.999 | yes | 0.001 | 0.000 | 0.000407 | 0.000407 | 1.625 | 0.999 |
| Women's | FS | v_on | 30 min | 1.000 | 0.998 to 1.000 | over-covers | no | 1.000 | yes | 0.001 | 0.000 | 0.000456 | 0.000456 | 1.826 | 1.000 |
| Women's | FS | v_on | 60 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000597 | 0.000597 | 2.386 | 1.000 |
| Women's | FS | v_on | 180 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000888 | 0.000887 | 3.534 | 1.000 |
| Women's | S | ips_ratio | rows | 0.950 | 0.943 to 0.956 | adequate | yes | 0.951 | yes | 0.028 | 0.022 | 0.125 | 0.125 | 0.994 | 0.950 |
| Women's | S | ips_ratio | impressions | 0.953 | 0.946 to 0.959 | adequate | yes | 0.951 | yes | 0.025 | 0.022 | 0.125 | 0.125 | 0.995 | 0.953 |
| Women's | S | ips_ratio | 5 min | 0.957 | 0.950 to 0.963 | adequate | yes | 0.958 | yes | 0.025 | 0.019 | 0.128 | 0.128 | 1.025 | 0.956 |
| Women's | S | ips_ratio | 10 min | 0.962 | 0.955 to 0.967 | adequate | no | 0.961 | yes | 0.022 | 0.017 | 0.131 | 0.131 | 1.046 | 0.962 |
| Women's | S | ips_ratio | 20 min | 0.968 | 0.962 to 0.973 | adequate | no | 0.967 | yes | 0.018 | 0.014 | 0.135 | 0.135 | 1.082 | 0.967 |
| Women's | S | ips_ratio | 30 min | 0.968 | 0.962 to 0.973 | adequate | no | 0.972 | yes | 0.018 | 0.014 | 0.138 | 0.138 | 1.103 | 0.967 |
| Women's | S | ips_ratio | 60 min | 0.979 | 0.974 to 0.983 | unresolved | no | 0.982 | yes | 0.012 | 0.009 | 0.149 | 0.149 | 1.190 | 0.980 |
| Women's | S | ips_ratio | 180 min | 0.993 | 0.990 to 0.995 | over-covers | no | 0.995 | no | 0.004 | 0.004 | 0.176 | 0.176 | 1.411 | 0.993 |
| Women's | S | snips_ratio | rows | 0.949 | 0.942 to 0.956 | adequate | yes | 0.950 | yes | 0.028 | 0.023 | 0.124 | 0.124 | 0.992 | 0.949 |
| Women's | S | snips_ratio | impressions | 0.951 | 0.944 to 0.957 | adequate | yes | 0.950 | yes | 0.026 | 0.023 | 0.124 | 0.124 | 0.992 | 0.951 |
| Women's | S | snips_ratio | 5 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.954 | yes | 0.026 | 0.021 | 0.126 | 0.126 | 1.008 | 0.953 |
| Women's | S | snips_ratio | 10 min | 0.957 | 0.950 to 0.962 | adequate | yes | 0.958 | yes | 0.024 | 0.019 | 0.128 | 0.128 | 1.025 | 0.956 |
| Women's | S | snips_ratio | 20 min | 0.962 | 0.956 to 0.968 | adequate | no | 0.964 | yes | 0.021 | 0.017 | 0.133 | 0.133 | 1.060 | 0.962 |
| Women's | S | snips_ratio | 30 min | 0.964 | 0.958 to 0.969 | adequate | no | 0.969 | yes | 0.019 | 0.017 | 0.136 | 0.136 | 1.084 | 0.965 |
| Women's | S | snips_ratio | 60 min | 0.976 | 0.971 to 0.980 | unresolved | no | 0.980 | yes | 0.013 | 0.011 | 0.146 | 0.146 | 1.168 | 0.976 |
| Women's | S | snips_ratio | 180 min | 0.992 | 0.988 to 0.994 | over-covers | no | 0.994 | no | 0.004 | 0.004 | 0.173 | 0.173 | 1.386 | 0.992 |
| Women's | S | ips | rows | 0.949 | 0.941 to 0.955 | adequate | yes | 0.951 | yes | 0.029 | 0.022 | 0.000786 | 0.000786 | 0.996 | 0.948 |
| Women's | S | ips | impressions | 0.949 | 0.942 to 0.956 | adequate | yes | 0.951 | yes | 0.028 | 0.022 | 0.000787 | 0.000786 | 0.997 | 0.950 |
| Women's | S | ips | 5 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.954 | yes | 0.028 | 0.021 | 0.000798 | 0.000798 | 1.012 | 0.952 |
| Women's | S | ips | 10 min | 0.956 | 0.949 to 0.961 | adequate | yes | 0.955 | yes | 0.025 | 0.019 | 0.000799 | 0.000798 | 1.013 | 0.955 |
| Women's | S | ips | 20 min | 0.953 | 0.945 to 0.959 | adequate | yes | 0.955 | yes | 0.025 | 0.022 | 0.000801 | 0.0008 | 1.015 | 0.952 |
| Women's | S | ips | 30 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.955 | yes | 0.028 | 0.020 | 0.0008 | 0.0008 | 1.015 | 0.952 |
| Women's | S | ips | 60 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.956 | yes | 0.030 | 0.019 | 0.000801 | 0.0008 | 1.014 | 0.951 |
| Women's | S | ips | 180 min | 0.945 | 0.938 to 0.952 | adequate | yes | 0.956 | no | 0.032 | 0.023 | 0.000792 | 0.000789 | 1.003 | 0.945 |
| Women's | S | v_on | rows | 0.948 | 0.940 to 0.954 | adequate | yes | 0.950 | yes | 0.027 | 0.025 | 0.000112 | 0.000112 | 1.001 | 0.948 |
| Women's | S | v_on | impressions | 0.950 | 0.943 to 0.956 | adequate | yes | 0.950 | yes | 0.025 | 0.025 | 0.000112 | 0.000112 | 1.002 | 0.950 |
| Women's | S | v_on | 5 min | 0.999 | 0.997 to 1.000 | over-covers | no | 0.999 | yes | 0.001 | 0.001 | 0.000184 | 0.000184 | 1.652 | 0.999 |
| Women's | S | v_on | 10 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000235 | 0.000235 | 2.114 | 1.000 |
| Women's | S | v_on | 20 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000316 | 0.000316 | 2.842 | 1.000 |
| Women's | S | v_on | 30 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000367 | 0.000367 | 3.308 | 1.000 |
| Women's | S | v_on | 60 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000509 | 0.000509 | 4.557 | 1.000 |
| Women's | S | v_on | 180 min | 1.000 | 0.999 to 1.000 | over-covers | no | 1.000 | yes | 0.000 | 0.000 | 0.000787 | 0.000787 | 7.022 | 1.000 |
| Women's | M.half-sessions | ips_ratio | rows | 0.903 | 0.893 to 0.912 | under-covers | no | 0.895 | yes | 0.051 | 0.046 | 0.124 | 0.124 | 0.851 | 0.903 |
| Women's | M.half-sessions | ips_ratio | impressions | 0.911 | 0.902 to 0.920 | under-covers | no | 0.907 | yes | 0.048 | 0.041 | 0.129 | 0.129 | 0.879 | 0.911 |
| Women's | M.half-sessions | ips_ratio | 5 min | 0.951 | 0.944 to 0.958 | adequate | yes | 0.949 | yes | 0.027 | 0.022 | 0.149 | 0.149 | 1.021 | 0.952 |
| Women's | M.half-sessions | ips_ratio | 10 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.951 | yes | 0.025 | 0.021 | 0.151 | 0.151 | 1.031 | 0.954 |
| Women's | M.half-sessions | ips_ratio | 20 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.952 | yes | 0.024 | 0.021 | 0.152 | 0.151 | 1.037 | 0.955 |
| Women's | M.half-sessions | ips_ratio | 30 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.953 | yes | 0.025 | 0.021 | 0.152 | 0.152 | 1.038 | 0.955 |
| Women's | M.half-sessions | ips_ratio | 60 min | 0.954 | 0.947 to 0.960 | adequate | yes | 0.954 | yes | 0.025 | 0.021 | 0.152 | 0.152 | 1.039 | 0.955 |
| Women's | M.half-sessions | ips_ratio | 180 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.954 | no | 0.030 | 0.025 | 0.151 | 0.15 | 1.032 | 0.946 |
| Women's | M.half-sessions | snips_ratio | rows | 0.902 | 0.893 to 0.911 | under-covers | no | 0.894 | yes | 0.051 | 0.047 | 0.124 | 0.124 | 0.849 | 0.902 |
| Women's | M.half-sessions | snips_ratio | impressions | 0.910 | 0.901 to 0.919 | under-covers | no | 0.906 | yes | 0.048 | 0.042 | 0.128 | 0.128 | 0.877 | 0.910 |
| Women's | M.half-sessions | snips_ratio | 5 min | 0.949 | 0.942 to 0.955 | adequate | yes | 0.946 | yes | 0.028 | 0.023 | 0.147 | 0.147 | 1.009 | 0.949 |
| Women's | M.half-sessions | snips_ratio | 10 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.948 | yes | 0.026 | 0.022 | 0.149 | 0.148 | 1.017 | 0.952 |
| Women's | M.half-sessions | snips_ratio | 20 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.949 | yes | 0.025 | 0.022 | 0.149 | 0.149 | 1.022 | 0.953 |
| Women's | M.half-sessions | snips_ratio | 30 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.950 | yes | 0.026 | 0.022 | 0.15 | 0.149 | 1.023 | 0.952 |
| Women's | M.half-sessions | snips_ratio | 60 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.950 | yes | 0.027 | 0.022 | 0.15 | 0.149 | 1.023 | 0.952 |
| Women's | M.half-sessions | snips_ratio | 180 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.951 | yes | 0.029 | 0.024 | 0.149 | 0.148 | 1.018 | 0.947 |
| Women's | M.half-sessions | ips | rows | 0.909 | 0.900 to 0.918 | under-covers | no | 0.900 | no | 0.048 | 0.043 | 0.000786 | 0.000785 | 0.858 | 0.909 |
| Women's | M.half-sessions | ips | impressions | 0.919 | 0.910 to 0.927 | unresolved | no | 0.910 | no | 0.043 | 0.038 | 0.00081 | 0.00081 | 0.883 | 0.918 |
| Women's | M.half-sessions | ips | 5 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.949 | yes | 0.027 | 0.021 | 0.000933 | 0.000932 | 1.018 | 0.952 |
| Women's | M.half-sessions | ips | 10 min | 0.955 | 0.948 to 0.961 | adequate | yes | 0.952 | yes | 0.025 | 0.019 | 0.000941 | 0.00094 | 1.027 | 0.954 |
| Women's | M.half-sessions | ips | 20 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.953 | yes | 0.027 | 0.020 | 0.000945 | 0.000943 | 1.032 | 0.954 |
| Women's | M.half-sessions | ips | 30 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.953 | yes | 0.027 | 0.020 | 0.000947 | 0.000945 | 1.033 | 0.954 |
| Women's | M.half-sessions | ips | 60 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.954 | yes | 0.027 | 0.020 | 0.000947 | 0.000946 | 1.034 | 0.953 |
| Women's | M.half-sessions | ips | 180 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.031 | 0.022 | 0.000937 | 0.000931 | 1.023 | 0.946 |
| Women's | M.half-sessions | v_on | rows | 0.735 | 0.721 to 0.748 | under-covers | no | 0.725 | yes | 0.130 | 0.135 | 0.000112 | 0.000112 | 0.571 | 0.735 |
| Women's | M.half-sessions | v_on | impressions | 0.813 | 0.801 to 0.825 | under-covers | no | 0.802 | yes | 0.090 | 0.097 | 0.000132 | 0.000132 | 0.675 | 0.814 |
| Women's | M.half-sessions | v_on | 5 min | 0.949 | 0.942 to 0.956 | adequate | yes | 0.941 | no | 0.023 | 0.028 | 0.000194 | 0.000194 | 0.990 | 0.949 |
| Women's | M.half-sessions | v_on | 10 min | 0.953 | 0.946 to 0.959 | adequate | yes | 0.947 | yes | 0.022 | 0.025 | 0.000198 | 0.000198 | 1.012 | 0.954 |
| Women's | M.half-sessions | v_on | 20 min | 0.957 | 0.951 to 0.963 | adequate | no | 0.951 | yes | 0.020 | 0.023 | 0.000201 | 0.000201 | 1.030 | 0.958 |
| Women's | M.half-sessions | v_on | 30 min | 0.959 | 0.952 to 0.964 | adequate | no | 0.954 | yes | 0.019 | 0.022 | 0.000203 | 0.000203 | 1.038 | 0.958 |
| Women's | M.half-sessions | v_on | 60 min | 0.963 | 0.956 to 0.968 | adequate | no | 0.959 | yes | 0.018 | 0.019 | 0.000207 | 0.000207 | 1.060 | 0.963 |
| Women's | M.half-sessions | v_on | 180 min | 0.970 | 0.964 to 0.975 | adequate | no | 0.971 | yes | 0.017 | 0.013 | 0.00022 | 0.00022 | 1.126 | 0.969 |
| Women's | M.double-sessions | ips_ratio | rows | 0.851 | 0.840 to 0.862 | under-covers | no | 0.847 | yes | 0.074 | 0.075 | 0.125 | 0.124 | 0.728 | 0.851 |
| Women's | M.double-sessions | ips_ratio | impressions | 0.863 | 0.852 to 0.873 | under-covers | no | 0.860 | yes | 0.069 | 0.069 | 0.129 | 0.129 | 0.753 | 0.863 |
| Women's | M.double-sessions | ips_ratio | 5 min | 0.944 | 0.937 to 0.951 | adequate | yes | 0.946 | yes | 0.029 | 0.026 | 0.168 | 0.167 | 0.981 | 0.944 |
| Women's | M.double-sessions | ips_ratio | 10 min | 0.948 | 0.941 to 0.955 | adequate | yes | 0.950 | yes | 0.027 | 0.025 | 0.17 | 0.17 | 0.997 | 0.948 |
| Women's | M.double-sessions | ips_ratio | 20 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.951 | yes | 0.027 | 0.026 | 0.172 | 0.171 | 1.004 | 0.947 |
| Women's | M.double-sessions | ips_ratio | 30 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.952 | yes | 0.026 | 0.022 | 0.172 | 0.171 | 1.005 | 0.952 |
| Women's | M.double-sessions | ips_ratio | 60 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.953 | yes | 0.029 | 0.024 | 0.172 | 0.172 | 1.008 | 0.947 |
| Women's | M.double-sessions | ips_ratio | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.953 | yes | 0.026 | 0.027 | 0.171 | 0.17 | 1.000 | 0.947 |
| Women's | M.double-sessions | snips_ratio | rows | 0.848 | 0.837 to 0.859 | under-covers | no | 0.845 | yes | 0.076 | 0.075 | 0.124 | 0.124 | 0.726 | 0.848 |
| Women's | M.double-sessions | snips_ratio | impressions | 0.862 | 0.851 to 0.872 | under-covers | no | 0.859 | yes | 0.069 | 0.069 | 0.128 | 0.128 | 0.751 | 0.862 |
| Women's | M.double-sessions | snips_ratio | 5 min | 0.942 | 0.934 to 0.948 | adequate | no | 0.943 | yes | 0.031 | 0.028 | 0.166 | 0.166 | 0.972 | 0.942 |
| Women's | M.double-sessions | snips_ratio | 10 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.947 | yes | 0.028 | 0.027 | 0.168 | 0.168 | 0.986 | 0.945 |
| Women's | M.double-sessions | snips_ratio | 20 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.949 | yes | 0.027 | 0.027 | 0.17 | 0.169 | 0.992 | 0.946 |
| Women's | M.double-sessions | snips_ratio | 30 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.949 | yes | 0.028 | 0.025 | 0.17 | 0.169 | 0.993 | 0.948 |
| Women's | M.double-sessions | snips_ratio | 60 min | 0.944 | 0.936 to 0.951 | adequate | yes | 0.950 | yes | 0.029 | 0.026 | 0.17 | 0.169 | 0.995 | 0.944 |
| Women's | M.double-sessions | snips_ratio | 180 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.951 | no | 0.029 | 0.029 | 0.169 | 0.168 | 0.988 | 0.943 |
| Women's | M.double-sessions | ips | rows | 0.860 | 0.849 to 0.870 | under-covers | no | 0.855 | yes | 0.071 | 0.069 | 0.000786 | 0.000785 | 0.749 | 0.859 |
| Women's | M.double-sessions | ips | impressions | 0.874 | 0.863 to 0.884 | under-covers | no | 0.867 | yes | 0.065 | 0.062 | 0.00081 | 0.000809 | 0.771 | 0.874 |
| Women's | M.double-sessions | ips | 5 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.946 | yes | 0.029 | 0.023 | 0.00104 | 0.00104 | 0.991 | 0.948 |
| Women's | M.double-sessions | ips | 10 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.950 | yes | 0.028 | 0.022 | 0.00106 | 0.00105 | 1.006 | 0.949 |
| Women's | M.double-sessions | ips | 20 min | 0.950 | 0.943 to 0.957 | adequate | yes | 0.951 | yes | 0.028 | 0.022 | 0.00106 | 0.00106 | 1.012 | 0.950 |
| Women's | M.double-sessions | ips | 30 min | 0.951 | 0.944 to 0.958 | adequate | yes | 0.952 | yes | 0.028 | 0.021 | 0.00106 | 0.00106 | 1.013 | 0.951 |
| Women's | M.double-sessions | ips | 60 min | 0.951 | 0.943 to 0.957 | adequate | yes | 0.953 | yes | 0.028 | 0.021 | 0.00107 | 0.00106 | 1.015 | 0.950 |
| Women's | M.double-sessions | ips | 180 min | 0.945 | 0.937 to 0.952 | adequate | yes | 0.953 | no | 0.031 | 0.024 | 0.00106 | 0.00105 | 1.006 | 0.945 |
| Women's | M.double-sessions | v_on | rows | 0.591 | 0.576 to 0.606 | under-covers | no | 0.595 | yes | 0.208 | 0.201 | 0.000112 | 0.000112 | 0.428 | 0.593 |
| Women's | M.double-sessions | v_on | impressions | 0.679 | 0.665 to 0.694 | under-covers | no | 0.674 | yes | 0.164 | 0.156 | 0.000132 | 0.000132 | 0.505 | 0.680 |
| Women's | M.double-sessions | v_on | 5 min | 0.935 | 0.927 to 0.942 | adequate | no | 0.938 | yes | 0.035 | 0.030 | 0.00025 | 0.00025 | 0.958 | 0.935 |
| Women's | M.double-sessions | v_on | 10 min | 0.941 | 0.934 to 0.948 | adequate | no | 0.945 | yes | 0.032 | 0.026 | 0.000257 | 0.000257 | 0.984 | 0.943 |
| Women's | M.double-sessions | v_on | 20 min | 0.944 | 0.937 to 0.951 | adequate | yes | 0.949 | yes | 0.032 | 0.024 | 0.000261 | 0.000261 | 0.999 | 0.945 |
| Women's | M.double-sessions | v_on | 30 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.951 | yes | 0.029 | 0.023 | 0.000263 | 0.000262 | 1.006 | 0.948 |
| Women's | M.double-sessions | v_on | 60 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.955 | yes | 0.029 | 0.021 | 0.000266 | 0.000265 | 1.018 | 0.951 |
| Women's | M.double-sessions | v_on | 180 min | 0.953 | 0.945 to 0.959 | adequate | yes | 0.963 | no | 0.030 | 0.017 | 0.000275 | 0.000273 | 1.052 | 0.954 |
| Women's | M.two-level | ips_ratio | rows | 0.849 | 0.838 to 0.860 | under-covers | no | 0.850 | yes | 0.077 | 0.074 | 0.125 | 0.125 | 0.734 | 0.851 |
| Women's | M.two-level | ips_ratio | impressions | 0.864 | 0.853 to 0.874 | under-covers | no | 0.863 | yes | 0.069 | 0.067 | 0.129 | 0.129 | 0.758 | 0.863 |
| Women's | M.two-level | ips_ratio | 5 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.946 | yes | 0.033 | 0.024 | 0.166 | 0.166 | 0.979 | 0.942 |
| Women's | M.two-level | ips_ratio | 10 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.949 | yes | 0.032 | 0.024 | 0.169 | 0.168 | 0.993 | 0.945 |
| Women's | M.two-level | ips_ratio | 20 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.951 | yes | 0.030 | 0.022 | 0.17 | 0.169 | 1.000 | 0.946 |
| Women's | M.two-level | ips_ratio | 30 min | 0.949 | 0.942 to 0.956 | adequate | yes | 0.952 | yes | 0.030 | 0.021 | 0.17 | 0.169 | 1.001 | 0.949 |
| Women's | M.two-level | ips_ratio | 60 min | 0.949 | 0.942 to 0.955 | adequate | yes | 0.953 | yes | 0.030 | 0.021 | 0.17 | 0.17 | 1.004 | 0.948 |
| Women's | M.two-level | ips_ratio | 180 min | 0.944 | 0.936 to 0.951 | adequate | yes | 0.953 | no | 0.032 | 0.025 | 0.169 | 0.169 | 0.999 | 0.943 |
| Women's | M.two-level | snips_ratio | rows | 0.850 | 0.838 to 0.860 | under-covers | no | 0.849 | yes | 0.077 | 0.074 | 0.124 | 0.124 | 0.732 | 0.850 |
| Women's | M.two-level | snips_ratio | impressions | 0.861 | 0.850 to 0.872 | under-covers | no | 0.862 | yes | 0.070 | 0.069 | 0.128 | 0.128 | 0.756 | 0.862 |
| Women's | M.two-level | snips_ratio | 5 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.943 | yes | 0.034 | 0.026 | 0.164 | 0.164 | 0.969 | 0.940 |
| Women's | M.two-level | snips_ratio | 10 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.947 | yes | 0.034 | 0.026 | 0.167 | 0.166 | 0.982 | 0.940 |
| Women's | M.two-level | snips_ratio | 20 min | 0.944 | 0.937 to 0.951 | adequate | yes | 0.948 | yes | 0.032 | 0.024 | 0.168 | 0.167 | 0.988 | 0.945 |
| Women's | M.two-level | snips_ratio | 30 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.949 | yes | 0.032 | 0.022 | 0.168 | 0.167 | 0.989 | 0.946 |
| Women's | M.two-level | snips_ratio | 60 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.950 | yes | 0.032 | 0.023 | 0.168 | 0.167 | 0.990 | 0.946 |
| Women's | M.two-level | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.951 | no | 0.034 | 0.027 | 0.167 | 0.167 | 0.987 | 0.939 |
| Women's | M.two-level | ips | rows | 0.862 | 0.850 to 0.872 | under-covers | no | 0.857 | yes | 0.070 | 0.068 | 0.000787 | 0.000786 | 0.752 | 0.862 |
| Women's | M.two-level | ips | impressions | 0.871 | 0.860 to 0.881 | under-covers | no | 0.869 | yes | 0.064 | 0.065 | 0.00081 | 0.00081 | 0.774 | 0.872 |
| Women's | M.two-level | ips | 5 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.946 | yes | 0.034 | 0.026 | 0.00103 | 0.00103 | 0.987 | 0.941 |
| Women's | M.two-level | ips | 10 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.950 | yes | 0.031 | 0.024 | 0.00105 | 0.00104 | 1.000 | 0.945 |
| Women's | M.two-level | ips | 20 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.951 | yes | 0.031 | 0.024 | 0.00105 | 0.00105 | 1.007 | 0.946 |
| Women's | M.two-level | ips | 30 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.952 | yes | 0.030 | 0.022 | 0.00105 | 0.00105 | 1.008 | 0.948 |
| Women's | M.two-level | ips | 60 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.032 | 0.022 | 0.00106 | 0.00105 | 1.010 | 0.946 |
| Women's | M.two-level | ips | 180 min | 0.944 | 0.937 to 0.951 | adequate | yes | 0.953 | no | 0.032 | 0.024 | 0.00105 | 0.00104 | 1.004 | 0.943 |
| Women's | M.two-level | v_on | rows | 0.611 | 0.596 to 0.626 | under-covers | no | 0.617 | yes | 0.187 | 0.202 | 0.000112 | 0.000112 | 0.446 | 0.616 |
| Women's | M.two-level | v_on | impressions | 0.693 | 0.678 to 0.707 | under-covers | no | 0.697 | yes | 0.153 | 0.154 | 0.000132 | 0.000132 | 0.526 | 0.692 |
| Women's | M.two-level | v_on | 5 min | 0.936 | 0.928 to 0.943 | adequate | no | 0.938 | yes | 0.034 | 0.030 | 0.000239 | 0.000239 | 0.955 | 0.937 |
| Women's | M.two-level | v_on | 10 min | 0.945 | 0.938 to 0.952 | adequate | yes | 0.946 | yes | 0.030 | 0.024 | 0.000246 | 0.000246 | 0.981 | 0.945 |
| Women's | M.two-level | v_on | 20 min | 0.950 | 0.943 to 0.956 | adequate | yes | 0.949 | yes | 0.028 | 0.022 | 0.00025 | 0.000249 | 0.997 | 0.950 |
| Women's | M.two-level | v_on | 30 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.951 | yes | 0.028 | 0.021 | 0.000252 | 0.000251 | 1.005 | 0.951 |
| Women's | M.two-level | v_on | 60 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.955 | yes | 0.029 | 0.020 | 0.000255 | 0.000255 | 1.018 | 0.951 |
| Women's | M.two-level | v_on | 180 min | 0.958 | 0.951 to 0.963 | adequate | no | 0.965 | no | 0.026 | 0.017 | 0.000265 | 0.000263 | 1.059 | 0.957 |
| Women's | H.half-long | ips_ratio | rows | 0.748 | 0.734 to 0.761 | under-covers | no | 0.753 | yes | 0.134 | 0.118 | 0.124 | 0.124 | 0.585 | 0.748 |
| Women's | H.half-long | ips_ratio | impressions | 0.763 | 0.750 to 0.776 | under-covers | no | 0.768 | yes | 0.126 | 0.112 | 0.129 | 0.129 | 0.605 | 0.763 |
| Women's | H.half-long | ips_ratio | 5 min | 0.880 | 0.869 to 0.889 | under-covers | no | 0.884 | yes | 0.062 | 0.059 | 0.169 | 0.168 | 0.793 | 0.880 |
| Women's | H.half-long | ips_ratio | 10 min | 0.894 | 0.884 to 0.903 | under-covers | no | 0.896 | yes | 0.057 | 0.049 | 0.175 | 0.174 | 0.821 | 0.895 |
| Women's | H.half-long | ips_ratio | 20 min | 0.910 | 0.900 to 0.918 | under-covers | no | 0.910 | yes | 0.047 | 0.043 | 0.182 | 0.182 | 0.857 | 0.910 |
| Women's | H.half-long | ips_ratio | 30 min | 0.917 | 0.908 to 0.925 | unresolved | no | 0.920 | yes | 0.045 | 0.038 | 0.188 | 0.187 | 0.882 | 0.917 |
| Women's | H.half-long | ips_ratio | 60 min | 0.934 | 0.926 to 0.941 | adequate | no | 0.936 | yes | 0.035 | 0.031 | 0.198 | 0.197 | 0.932 | 0.934 |
| Women's | H.half-long | ips_ratio | 180 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.947 | no | 0.033 | 0.029 | 0.204 | 0.203 | 0.962 | 0.938 |
| Women's | H.half-long | snips_ratio | rows | 0.747 | 0.733 to 0.760 | under-covers | no | 0.751 | yes | 0.135 | 0.118 | 0.124 | 0.124 | 0.583 | 0.746 |
| Women's | H.half-long | snips_ratio | impressions | 0.763 | 0.750 to 0.776 | under-covers | no | 0.767 | yes | 0.126 | 0.112 | 0.128 | 0.128 | 0.603 | 0.763 |
| Women's | H.half-long | snips_ratio | 5 min | 0.875 | 0.864 to 0.885 | under-covers | no | 0.880 | yes | 0.064 | 0.061 | 0.167 | 0.167 | 0.785 | 0.875 |
| Women's | H.half-long | snips_ratio | 10 min | 0.889 | 0.879 to 0.899 | under-covers | no | 0.892 | yes | 0.058 | 0.052 | 0.173 | 0.172 | 0.812 | 0.889 |
| Women's | H.half-long | snips_ratio | 20 min | 0.907 | 0.898 to 0.916 | under-covers | no | 0.907 | yes | 0.048 | 0.044 | 0.18 | 0.18 | 0.848 | 0.907 |
| Women's | H.half-long | snips_ratio | 30 min | 0.912 | 0.903 to 0.920 | under-covers | no | 0.917 | yes | 0.047 | 0.041 | 0.186 | 0.185 | 0.874 | 0.912 |
| Women's | H.half-long | snips_ratio | 60 min | 0.930 | 0.922 to 0.938 | unresolved | no | 0.934 | yes | 0.037 | 0.033 | 0.196 | 0.196 | 0.923 | 0.930 |
| Women's | H.half-long | snips_ratio | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.945 | no | 0.033 | 0.030 | 0.203 | 0.202 | 0.955 | 0.937 |
| Women's | H.half-long | ips | rows | 0.758 | 0.744 to 0.771 | under-covers | no | 0.765 | yes | 0.126 | 0.117 | 0.000786 | 0.000785 | 0.602 | 0.758 |
| Women's | H.half-long | ips | impressions | 0.773 | 0.760 to 0.786 | under-covers | no | 0.779 | yes | 0.118 | 0.108 | 0.00081 | 0.00081 | 0.621 | 0.772 |
| Women's | H.half-long | ips | 5 min | 0.883 | 0.873 to 0.893 | under-covers | no | 0.887 | yes | 0.062 | 0.055 | 0.00105 | 0.00105 | 0.802 | 0.883 |
| Women's | H.half-long | ips | 10 min | 0.894 | 0.884 to 0.903 | under-covers | no | 0.899 | yes | 0.058 | 0.048 | 0.00108 | 0.00108 | 0.829 | 0.895 |
| Women's | H.half-long | ips | 20 min | 0.909 | 0.900 to 0.918 | under-covers | no | 0.912 | yes | 0.048 | 0.043 | 0.00113 | 0.00113 | 0.864 | 0.910 |
| Women's | H.half-long | ips | 30 min | 0.915 | 0.906 to 0.923 | under-covers | no | 0.921 | yes | 0.045 | 0.040 | 0.00116 | 0.00116 | 0.888 | 0.916 |
| Women's | H.half-long | ips | 60 min | 0.930 | 0.921 to 0.937 | unresolved | no | 0.937 | yes | 0.039 | 0.032 | 0.00122 | 0.00122 | 0.936 | 0.929 |
| Women's | H.half-long | ips | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.947 | no | 0.036 | 0.026 | 0.00126 | 0.00125 | 0.964 | 0.937 |
| Women's | H.half-long | v_on | rows | 0.465 | 0.450 to 0.481 | under-covers | no | 0.461 | yes | 0.277 | 0.258 | 0.000112 | 0.000112 | 0.318 | 0.468 |
| Women's | H.half-long | v_on | impressions | 0.543 | 0.528 to 0.558 | under-covers | no | 0.532 | yes | 0.240 | 0.217 | 0.000132 | 0.000132 | 0.375 | 0.538 |
| Women's | H.half-long | v_on | 5 min | 0.827 | 0.815 to 0.838 | under-covers | no | 0.825 | yes | 0.092 | 0.082 | 0.000246 | 0.000246 | 0.700 | 0.825 |
| Women's | H.half-long | v_on | 10 min | 0.849 | 0.837 to 0.860 | under-covers | no | 0.852 | yes | 0.082 | 0.070 | 0.000262 | 0.000262 | 0.745 | 0.850 |
| Women's | H.half-long | v_on | 20 min | 0.877 | 0.867 to 0.887 | under-covers | no | 0.881 | yes | 0.067 | 0.056 | 0.000282 | 0.000282 | 0.803 | 0.876 |
| Women's | H.half-long | v_on | 30 min | 0.897 | 0.888 to 0.907 | under-covers | no | 0.900 | yes | 0.056 | 0.046 | 0.000297 | 0.000297 | 0.846 | 0.897 |
| Women's | H.half-long | v_on | 60 min | 0.927 | 0.919 to 0.935 | unresolved | no | 0.929 | yes | 0.041 | 0.032 | 0.000325 | 0.000324 | 0.926 | 0.926 |
| Women's | H.half-long | v_on | 180 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.951 | yes | 0.031 | 0.023 | 0.000352 | 0.000349 | 1.001 | 0.947 |
| Women's | H.double-long | ips_ratio | rows | 0.656 | 0.642 to 0.671 | under-covers | no | 0.654 | yes | 0.172 | 0.171 | 0.125 | 0.125 | 0.487 | 0.653 |
| Women's | H.double-long | ips_ratio | impressions | 0.674 | 0.660 to 0.689 | under-covers | no | 0.670 | yes | 0.164 | 0.162 | 0.129 | 0.129 | 0.503 | 0.673 |
| Women's | H.double-long | ips_ratio | 5 min | 0.813 | 0.800 to 0.825 | under-covers | no | 0.809 | yes | 0.100 | 0.087 | 0.173 | 0.172 | 0.675 | 0.812 |
| Women's | H.double-long | ips_ratio | 10 min | 0.839 | 0.827 to 0.850 | under-covers | no | 0.835 | yes | 0.084 | 0.077 | 0.183 | 0.183 | 0.715 | 0.839 |
| Women's | H.double-long | ips_ratio | 20 min | 0.873 | 0.862 to 0.882 | under-covers | no | 0.868 | yes | 0.068 | 0.060 | 0.199 | 0.198 | 0.777 | 0.873 |
| Women's | H.double-long | ips_ratio | 30 min | 0.894 | 0.884 to 0.903 | under-covers | no | 0.889 | yes | 0.060 | 0.045 | 0.21 | 0.209 | 0.819 | 0.894 |
| Women's | H.double-long | ips_ratio | 60 min | 0.918 | 0.909 to 0.926 | unresolved | no | 0.921 | yes | 0.048 | 0.035 | 0.23 | 0.229 | 0.899 | 0.917 |
| Women's | H.double-long | ips_ratio | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.942 | yes | 0.035 | 0.028 | 0.246 | 0.244 | 0.964 | 0.936 |
| Women's | H.double-long | snips_ratio | rows | 0.653 | 0.639 to 0.668 | under-covers | no | 0.653 | yes | 0.173 | 0.173 | 0.124 | 0.124 | 0.485 | 0.652 |
| Women's | H.double-long | snips_ratio | impressions | 0.672 | 0.657 to 0.686 | under-covers | no | 0.669 | yes | 0.165 | 0.164 | 0.128 | 0.128 | 0.502 | 0.672 |
| Women's | H.double-long | snips_ratio | 5 min | 0.810 | 0.798 to 0.822 | under-covers | no | 0.805 | yes | 0.102 | 0.088 | 0.171 | 0.171 | 0.668 | 0.808 |
| Women's | H.double-long | snips_ratio | 10 min | 0.835 | 0.823 to 0.846 | under-covers | no | 0.831 | yes | 0.086 | 0.079 | 0.181 | 0.181 | 0.708 | 0.834 |
| Women's | H.double-long | snips_ratio | 20 min | 0.870 | 0.859 to 0.880 | under-covers | no | 0.865 | yes | 0.070 | 0.060 | 0.197 | 0.196 | 0.770 | 0.870 |
| Women's | H.double-long | snips_ratio | 30 min | 0.891 | 0.881 to 0.900 | under-covers | no | 0.886 | yes | 0.061 | 0.048 | 0.208 | 0.207 | 0.813 | 0.890 |
| Women's | H.double-long | snips_ratio | 60 min | 0.916 | 0.907 to 0.924 | under-covers | no | 0.918 | yes | 0.049 | 0.035 | 0.228 | 0.227 | 0.893 | 0.915 |
| Women's | H.double-long | snips_ratio | 180 min | 0.933 | 0.925 to 0.941 | adequate | no | 0.941 | yes | 0.036 | 0.030 | 0.245 | 0.243 | 0.958 | 0.935 |
| Women's | H.double-long | ips | rows | 0.665 | 0.650 to 0.679 | under-covers | no | 0.669 | yes | 0.168 | 0.167 | 0.000786 | 0.000785 | 0.499 | 0.665 |
| Women's | H.double-long | ips | impressions | 0.679 | 0.665 to 0.694 | under-covers | no | 0.684 | yes | 0.163 | 0.158 | 0.00081 | 0.00081 | 0.514 | 0.678 |
| Women's | H.double-long | ips | 5 min | 0.807 | 0.795 to 0.819 | under-covers | no | 0.815 | yes | 0.104 | 0.088 | 0.00107 | 0.00107 | 0.679 | 0.808 |
| Women's | H.double-long | ips | 10 min | 0.838 | 0.826 to 0.849 | under-covers | no | 0.840 | yes | 0.086 | 0.076 | 0.00113 | 0.00113 | 0.718 | 0.836 |
| Women's | H.double-long | ips | 20 min | 0.867 | 0.856 to 0.877 | under-covers | no | 0.872 | yes | 0.071 | 0.061 | 0.00122 | 0.00122 | 0.777 | 0.867 |
| Women's | H.double-long | ips | 30 min | 0.888 | 0.878 to 0.897 | under-covers | no | 0.891 | yes | 0.062 | 0.050 | 0.00129 | 0.00128 | 0.817 | 0.889 |
| Women's | H.double-long | ips | 60 min | 0.920 | 0.911 to 0.928 | unresolved | no | 0.921 | yes | 0.045 | 0.035 | 0.00141 | 0.0014 | 0.893 | 0.918 |
| Women's | H.double-long | ips | 180 min | 0.936 | 0.928 to 0.943 | adequate | no | 0.942 | yes | 0.037 | 0.027 | 0.0015 | 0.00149 | 0.954 | 0.936 |
| Women's | H.double-long | v_on | rows | 0.364 | 0.349 to 0.379 | under-covers | no | 0.360 | yes | 0.309 | 0.327 | 0.000112 | 0.000112 | 0.240 | 0.363 |
| Women's | H.double-long | v_on | impressions | 0.425 | 0.410 to 0.441 | under-covers | no | 0.419 | yes | 0.280 | 0.294 | 0.000132 | 0.000132 | 0.283 | 0.425 |
| Women's | H.double-long | v_on | 5 min | 0.716 | 0.701 to 0.729 | under-covers | no | 0.717 | yes | 0.147 | 0.137 | 0.000256 | 0.000256 | 0.550 | 0.716 |
| Women's | H.double-long | v_on | 10 min | 0.764 | 0.750 to 0.777 | under-covers | no | 0.768 | yes | 0.123 | 0.113 | 0.000284 | 0.000284 | 0.610 | 0.763 |
| Women's | H.double-long | v_on | 20 min | 0.817 | 0.805 to 0.829 | under-covers | no | 0.827 | yes | 0.094 | 0.089 | 0.000324 | 0.000323 | 0.696 | 0.818 |
| Women's | H.double-long | v_on | 30 min | 0.858 | 0.847 to 0.868 | under-covers | no | 0.864 | yes | 0.072 | 0.070 | 0.000354 | 0.000353 | 0.760 | 0.858 |
| Women's | H.double-long | v_on | 60 min | 0.911 | 0.902 to 0.920 | under-covers | no | 0.914 | yes | 0.048 | 0.041 | 0.000407 | 0.000406 | 0.874 | 0.910 |
| Women's | H.double-long | v_on | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.944 | no | 0.035 | 0.027 | 0.00045 | 0.000447 | 0.966 | 0.936 |
| Women's | H.two-level | ips_ratio | rows | 0.687 | 0.672 to 0.701 | under-covers | no | 0.679 | yes | 0.170 | 0.143 | 0.124 | 0.124 | 0.515 | 0.692 |
| Women's | H.two-level | ips_ratio | impressions | 0.701 | 0.687 to 0.715 | under-covers | no | 0.695 | yes | 0.163 | 0.137 | 0.128 | 0.128 | 0.532 | 0.703 |
| Women's | H.two-level | ips_ratio | 5 min | 0.830 | 0.818 to 0.841 | under-covers | no | 0.829 | yes | 0.100 | 0.070 | 0.171 | 0.171 | 0.707 | 0.830 |
| Women's | H.two-level | ips_ratio | 10 min | 0.852 | 0.841 to 0.863 | under-covers | no | 0.851 | yes | 0.088 | 0.059 | 0.18 | 0.179 | 0.744 | 0.851 |
| Women's | H.two-level | ips_ratio | 20 min | 0.876 | 0.866 to 0.886 | under-covers | no | 0.879 | yes | 0.075 | 0.049 | 0.193 | 0.192 | 0.799 | 0.878 |
| Women's | H.two-level | ips_ratio | 30 min | 0.890 | 0.880 to 0.900 | under-covers | no | 0.897 | yes | 0.068 | 0.042 | 0.202 | 0.201 | 0.838 | 0.893 |
| Women's | H.two-level | ips_ratio | 60 min | 0.921 | 0.912 to 0.929 | unresolved | no | 0.925 | yes | 0.051 | 0.028 | 0.22 | 0.219 | 0.911 | 0.920 |
| Women's | H.two-level | ips_ratio | 180 min | 0.934 | 0.926 to 0.941 | adequate | no | 0.943 | no | 0.044 | 0.021 | 0.233 | 0.23 | 0.965 | 0.936 |
| Women's | H.two-level | snips_ratio | rows | 0.686 | 0.671 to 0.700 | under-covers | no | 0.678 | yes | 0.170 | 0.144 | 0.124 | 0.124 | 0.514 | 0.690 |
| Women's | H.two-level | snips_ratio | impressions | 0.701 | 0.686 to 0.714 | under-covers | no | 0.694 | yes | 0.163 | 0.136 | 0.128 | 0.128 | 0.531 | 0.702 |
| Women's | H.two-level | snips_ratio | 5 min | 0.828 | 0.815 to 0.839 | under-covers | no | 0.825 | yes | 0.100 | 0.072 | 0.169 | 0.169 | 0.700 | 0.826 |
| Women's | H.two-level | snips_ratio | 10 min | 0.849 | 0.837 to 0.859 | under-covers | no | 0.847 | yes | 0.089 | 0.062 | 0.178 | 0.177 | 0.737 | 0.848 |
| Women's | H.two-level | snips_ratio | 20 min | 0.873 | 0.863 to 0.883 | under-covers | no | 0.876 | yes | 0.077 | 0.050 | 0.191 | 0.19 | 0.792 | 0.875 |
| Women's | H.two-level | snips_ratio | 30 min | 0.889 | 0.879 to 0.898 | under-covers | no | 0.894 | yes | 0.069 | 0.042 | 0.201 | 0.2 | 0.831 | 0.890 |
| Women's | H.two-level | snips_ratio | 60 min | 0.918 | 0.909 to 0.926 | unresolved | no | 0.923 | yes | 0.052 | 0.030 | 0.218 | 0.217 | 0.905 | 0.919 |
| Women's | H.two-level | snips_ratio | 180 min | 0.932 | 0.924 to 0.940 | unresolved | no | 0.942 | no | 0.044 | 0.023 | 0.231 | 0.229 | 0.960 | 0.935 |
| Women's | H.two-level | ips | rows | 0.699 | 0.685 to 0.713 | under-covers | no | 0.694 | yes | 0.163 | 0.139 | 0.000786 | 0.000786 | 0.533 | 0.703 |
| Women's | H.two-level | ips | impressions | 0.709 | 0.695 to 0.723 | under-covers | no | 0.709 | yes | 0.160 | 0.131 | 0.000808 | 0.000808 | 0.548 | 0.712 |
| Women's | H.two-level | ips | 5 min | 0.839 | 0.827 to 0.850 | under-covers | no | 0.835 | yes | 0.096 | 0.065 | 0.00106 | 0.00106 | 0.718 | 0.841 |
| Women's | H.two-level | ips | 10 min | 0.858 | 0.847 to 0.868 | under-covers | no | 0.856 | yes | 0.084 | 0.058 | 0.00111 | 0.00111 | 0.754 | 0.860 |
| Women's | H.two-level | ips | 20 min | 0.881 | 0.871 to 0.891 | under-covers | no | 0.882 | yes | 0.071 | 0.048 | 0.00119 | 0.00118 | 0.807 | 0.883 |
| Women's | H.two-level | ips | 30 min | 0.894 | 0.884 to 0.903 | under-covers | no | 0.899 | yes | 0.065 | 0.042 | 0.00125 | 0.00124 | 0.844 | 0.895 |
| Women's | H.two-level | ips | 60 min | 0.919 | 0.910 to 0.927 | unresolved | no | 0.926 | yes | 0.053 | 0.028 | 0.00135 | 0.00134 | 0.916 | 0.921 |
| Women's | H.two-level | ips | 180 min | 0.934 | 0.926 to 0.942 | adequate | no | 0.943 | no | 0.044 | 0.021 | 0.00142 | 0.00141 | 0.967 | 0.935 |
| Women's | H.two-level | v_on | rows | 0.379 | 0.364 to 0.394 | under-covers | no | 0.383 | yes | 0.308 | 0.312 | 0.000112 | 0.000112 | 0.254 | 0.382 |
| Women's | H.two-level | v_on | impressions | 0.442 | 0.426 to 0.457 | under-covers | no | 0.446 | yes | 0.278 | 0.280 | 0.000132 | 0.000132 | 0.300 | 0.442 |
| Women's | H.two-level | v_on | 5 min | 0.738 | 0.724 to 0.752 | under-covers | no | 0.744 | yes | 0.133 | 0.129 | 0.000253 | 0.000253 | 0.576 | 0.738 |
| Women's | H.two-level | v_on | 10 min | 0.779 | 0.766 to 0.792 | under-covers | no | 0.788 | yes | 0.113 | 0.108 | 0.000277 | 0.000277 | 0.631 | 0.779 |
| Women's | H.two-level | v_on | 20 min | 0.831 | 0.819 to 0.842 | under-covers | no | 0.840 | yes | 0.089 | 0.080 | 0.000312 | 0.000311 | 0.709 | 0.831 |
| Women's | H.two-level | v_on | 30 min | 0.862 | 0.850 to 0.872 | under-covers | no | 0.872 | no | 0.073 | 0.066 | 0.000337 | 0.000336 | 0.768 | 0.862 |
| Women's | H.two-level | v_on | 60 min | 0.907 | 0.898 to 0.916 | under-covers | no | 0.917 | no | 0.048 | 0.045 | 0.000384 | 0.000383 | 0.873 | 0.906 |
| Women's | H.two-level | v_on | 180 min | 0.931 | 0.923 to 0.938 | unresolved | no | 0.946 | no | 0.038 | 0.031 | 0.000421 | 0.000418 | 0.959 | 0.931 |
| Men's | F | ips_ratio | rows | 0.908 | 0.899 to 0.917 | under-covers | no | 0.911 | yes | 0.053 | 0.039 | 0.145 | 0.145 | 0.865 | 0.908 |
| Men's | F | ips_ratio | impressions | 0.918 | 0.910 to 0.927 | unresolved | no | 0.920 | yes | 0.047 | 0.035 | 0.15 | 0.15 | 0.890 | 0.918 |
| Men's | F | ips_ratio | 5 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.952 | yes | 0.033 | 0.021 | 0.169 | 0.168 | 1.003 | 0.947 |
| Men's | F | ips_ratio | 10 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.034 | 0.021 | 0.169 | 0.169 | 1.005 | 0.946 |
| Men's | F | ips_ratio | 20 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.953 | yes | 0.032 | 0.021 | 0.169 | 0.169 | 1.008 | 0.948 |
| Men's | F | ips_ratio | 30 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.953 | yes | 0.032 | 0.020 | 0.17 | 0.169 | 1.010 | 0.948 |
| Men's | F | ips_ratio | 60 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.954 | no | 0.032 | 0.021 | 0.169 | 0.169 | 1.008 | 0.947 |
| Men's | F | ips_ratio | 180 min | 0.941 | 0.934 to 0.948 | adequate | no | 0.954 | no | 0.036 | 0.022 | 0.169 | 0.168 | 1.004 | 0.941 |
| Men's | F | snips_ratio | rows | 0.907 | 0.898 to 0.916 | under-covers | no | 0.910 | yes | 0.053 | 0.040 | 0.148 | 0.148 | 0.862 | 0.907 |
| Men's | F | snips_ratio | impressions | 0.917 | 0.908 to 0.925 | unresolved | no | 0.919 | yes | 0.048 | 0.035 | 0.152 | 0.152 | 0.888 | 0.918 |
| Men's | F | snips_ratio | 5 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.948 | yes | 0.033 | 0.024 | 0.169 | 0.169 | 0.989 | 0.944 |
| Men's | F | snips_ratio | 10 min | 0.943 | 0.936 to 0.950 | adequate | yes | 0.949 | yes | 0.035 | 0.022 | 0.17 | 0.169 | 0.991 | 0.944 |
| Men's | F | snips_ratio | 20 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.950 | yes | 0.035 | 0.021 | 0.17 | 0.17 | 0.994 | 0.945 |
| Men's | F | snips_ratio | 30 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.950 | yes | 0.035 | 0.022 | 0.17 | 0.17 | 0.994 | 0.943 |
| Men's | F | snips_ratio | 60 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.950 | yes | 0.033 | 0.022 | 0.17 | 0.169 | 0.992 | 0.944 |
| Men's | F | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.951 | no | 0.036 | 0.025 | 0.169 | 0.169 | 0.988 | 0.939 |
| Men's | F | ips | rows | 0.916 | 0.908 to 0.925 | under-covers | no | 0.920 | yes | 0.048 | 0.035 | 0.000966 | 0.000967 | 0.888 | 0.917 |
| Men's | F | ips | impressions | 0.924 | 0.916 to 0.932 | unresolved | no | 0.927 | yes | 0.045 | 0.031 | 0.000991 | 0.000991 | 0.911 | 0.924 |
| Men's | F | ips | 5 min | 0.948 | 0.940 to 0.954 | adequate | yes | 0.953 | yes | 0.033 | 0.019 | 0.00109 | 0.00109 | 1.005 | 0.948 |
| Men's | F | ips | 10 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.034 | 0.020 | 0.00109 | 0.00109 | 1.005 | 0.947 |
| Men's | F | ips | 20 min | 0.950 | 0.942 to 0.956 | adequate | yes | 0.953 | yes | 0.034 | 0.017 | 0.0011 | 0.00109 | 1.007 | 0.950 |
| Men's | F | ips | 30 min | 0.951 | 0.944 to 0.957 | adequate | yes | 0.954 | yes | 0.031 | 0.018 | 0.0011 | 0.0011 | 1.009 | 0.951 |
| Men's | F | ips | 60 min | 0.948 | 0.941 to 0.955 | adequate | yes | 0.954 | yes | 0.032 | 0.020 | 0.0011 | 0.00109 | 1.007 | 0.948 |
| Men's | F | ips | 180 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.954 | no | 0.037 | 0.022 | 0.00109 | 0.00109 | 1.002 | 0.941 |
| Men's | F | v_on | rows | 0.651 | 0.636 to 0.666 | under-covers | no | 0.644 | yes | 0.174 | 0.175 | 0.000158 | 0.000158 | 0.468 | 0.653 |
| Men's | F | v_on | impressions | 0.712 | 0.698 to 0.726 | under-covers | no | 0.713 | yes | 0.145 | 0.142 | 0.000183 | 0.000183 | 0.540 | 0.715 |
| Men's | F | v_on | 5 min | 0.932 | 0.924 to 0.940 | unresolved | no | 0.938 | yes | 0.035 | 0.033 | 0.00032 | 0.00032 | 0.947 | 0.934 |
| Men's | F | v_on | 10 min | 0.940 | 0.932 to 0.946 | adequate | no | 0.946 | yes | 0.032 | 0.028 | 0.000328 | 0.000328 | 0.971 | 0.940 |
| Men's | F | v_on | 20 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.949 | yes | 0.029 | 0.026 | 0.000333 | 0.000333 | 0.986 | 0.944 |
| Men's | F | v_on | 30 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.950 | yes | 0.029 | 0.025 | 0.000335 | 0.000334 | 0.990 | 0.945 |
| Men's | F | v_on | 60 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.029 | 0.025 | 0.000337 | 0.000336 | 0.997 | 0.948 |
| Men's | F | v_on | 180 min | 0.949 | 0.942 to 0.956 | adequate | yes | 0.960 | no | 0.029 | 0.022 | 0.000345 | 0.000343 | 1.021 | 0.949 |

## Cells whose prediction lies outside the Wilson interval

113 of 672 cells, the widest gap first.

| Campaign | Scenario | Quantity | Unit | Coverage | Wilson 95% | Label | Interval contains 0.95 | Predicted | Prediction inside | Interval below | Interval above | Mean width | Median width | sd of replicates / sd of estimate | Coverage of mean estimate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Women's | FH | v_on | 10 min | 0.603 | 0.588 to 0.618 | under-covers | no | 0.630 | no | 0.205 | 0.192 | 0.000363 | 0.000362 | 0.449 | 0.604 |
| Women's | FH | v_on | 5 min | 0.502 | 0.487 to 0.518 | under-covers | no | 0.524 | no | 0.254 | 0.243 | 0.00029 | 0.000289 | 0.358 | 0.503 |
| Women's | FH | v_on | 30 min | 0.796 | 0.783 to 0.808 | under-covers | no | 0.816 | no | 0.111 | 0.093 | 0.000537 | 0.000535 | 0.663 | 0.796 |
| Women's | FH | v_on | 20 min | 0.734 | 0.720 to 0.747 | under-covers | no | 0.751 | no | 0.143 | 0.123 | 0.000467 | 0.000466 | 0.577 | 0.733 |
| All | F | v_on | rows | 0.732 | 0.718 to 0.746 | under-covers | no | 0.716 | no | 0.138 | 0.130 | 7.81e-05 | 7.81e-05 | 0.554 | 0.732 |
| All | FH | v_on | impressions | 0.438 | 0.423 to 0.453 | under-covers | no | 0.454 | no | 0.280 | 0.282 | 8.43e-05 | 8.43e-05 | 0.306 | 0.439 |
| Women's | H.two-level | v_on | 180 min | 0.931 | 0.923 to 0.938 | unresolved | no | 0.946 | no | 0.038 | 0.031 | 0.000421 | 0.000418 | 0.959 | 0.931 |
| All | H.double-long | v_on | 180 min | 0.950 | 0.943 to 0.957 | adequate | yes | 0.965 | no | 0.030 | 0.019 | 0.000249 | 0.000248 | 1.040 | 0.950 |
| All | F | ips_ratio | 180 min | 0.942 | 0.934 to 0.948 | adequate | no | 0.955 | no | 0.034 | 0.025 | 0.147 | 0.147 | 0.993 | 0.942 |
| Women's | FH | v_on | 180 min | 0.923 | 0.915 to 0.931 | unresolved | no | 0.937 | no | 0.045 | 0.031 | 0.000742 | 0.000737 | 0.918 | 0.925 |
| All | FH | ips | 180 min | 0.936 | 0.928 to 0.943 | adequate | no | 0.950 | no | 0.034 | 0.030 | 0.000796 | 0.000792 | 0.968 | 0.937 |
| All | F | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.952 | no | 0.034 | 0.027 | 0.146 | 0.145 | 0.981 | 0.940 |
| Men's | F | ips | 180 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.954 | no | 0.037 | 0.022 | 0.00109 | 0.00109 | 1.002 | 0.941 |
| Men's | F | ips_ratio | 180 min | 0.941 | 0.934 to 0.948 | adequate | no | 0.954 | no | 0.036 | 0.022 | 0.169 | 0.168 | 1.004 | 0.941 |
| All | F | ips | 180 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.953 | no | 0.035 | 0.025 | 0.000711 | 0.000708 | 0.987 | 0.941 |
| All | FH | v_on | 180 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.958 | no | 0.034 | 0.022 | 0.000276 | 0.000275 | 1.003 | 0.946 |
| All | H.double-long | snips_ratio | 180 min | 0.935 | 0.927 to 0.942 | adequate | no | 0.947 | no | 0.035 | 0.030 | 0.191 | 0.189 | 0.959 | 0.935 |
| All | H.two-level | v_on | 180 min | 0.952 | 0.945 to 0.958 | adequate | yes | 0.965 | no | 0.025 | 0.022 | 0.000248 | 0.000247 | 1.035 | 0.952 |
| All | H.double-long | v_on | 10 min | 0.847 | 0.835 to 0.857 | under-covers | no | 0.859 | no | 0.080 | 0.074 | 0.000178 | 0.000178 | 0.741 | 0.847 |
| All | M.two-level | snips_ratio | rows | 0.873 | 0.862 to 0.883 | under-covers | no | 0.861 | no | 0.067 | 0.060 | 0.127 | 0.127 | 0.767 | 0.872 |
| All | H.double-long | v_on | 60 min | 0.927 | 0.918 to 0.934 | unresolved | no | 0.939 | no | 0.039 | 0.034 | 0.000225 | 0.000224 | 0.937 | 0.927 |
| All | H.double-long | ips_ratio | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.949 | no | 0.035 | 0.028 | 0.193 | 0.191 | 0.967 | 0.938 |
| Women's | M.two-level | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.951 | no | 0.034 | 0.027 | 0.167 | 0.167 | 0.987 | 0.939 |
| Men's | F | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.951 | no | 0.036 | 0.025 | 0.169 | 0.169 | 0.988 | 0.939 |
| Women's | FS | ips | 180 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.955 | no | 0.032 | 0.025 | 0.000852 | 0.000847 | 1.007 | 0.943 |
| All | M.half-sessions | snips_ratio | 180 min | 0.941 | 0.933 to 0.947 | adequate | no | 0.952 | no | 0.033 | 0.026 | 0.156 | 0.155 | 0.989 | 0.941 |
| Men's | F | v_on | 180 min | 0.949 | 0.942 to 0.956 | adequate | yes | 0.960 | no | 0.029 | 0.022 | 0.000345 | 0.000343 | 1.021 | 0.949 |
| All | M.two-level | ips_ratio | rows | 0.873 | 0.862 to 0.883 | under-covers | no | 0.862 | no | 0.067 | 0.060 | 0.127 | 0.127 | 0.769 | 0.873 |
| All | H.two-level | ips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.949 | no | 0.035 | 0.027 | 0.193 | 0.192 | 0.983 | 0.938 |
| Women's | M.double-sessions | v_on | 180 min | 0.953 | 0.945 to 0.959 | adequate | yes | 0.963 | no | 0.030 | 0.017 | 0.000275 | 0.000273 | 1.052 | 0.954 |
| All | M.double-sessions | v_on | 180 min | 0.970 | 0.964 to 0.975 | adequate | no | 0.981 | no | 0.019 | 0.011 | 0.000197 | 0.000196 | 1.160 | 0.969 |
| Women's | H.two-level | v_on | 30 min | 0.862 | 0.850 to 0.872 | under-covers | no | 0.872 | no | 0.073 | 0.066 | 0.000337 | 0.000336 | 0.768 | 0.862 |
| Women's | H.two-level | v_on | 60 min | 0.907 | 0.898 to 0.916 | under-covers | no | 0.917 | no | 0.048 | 0.045 | 0.000384 | 0.000383 | 0.873 | 0.906 |
| Women's | S | ips | 180 min | 0.945 | 0.938 to 0.952 | adequate | yes | 0.956 | no | 0.032 | 0.023 | 0.000792 | 0.000789 | 1.003 | 0.945 |
| All | H.double-long | v_on | 30 min | 0.898 | 0.888 to 0.907 | under-covers | no | 0.908 | no | 0.051 | 0.051 | 0.000203 | 0.000203 | 0.846 | 0.898 |
| All | M.double-sessions | v_on | 30 min | 0.948 | 0.941 to 0.954 | adequate | yes | 0.958 | no | 0.028 | 0.025 | 0.000174 | 0.000174 | 1.027 | 0.948 |
| Women's | M.half-sessions | ips | rows | 0.909 | 0.900 to 0.918 | under-covers | no | 0.900 | no | 0.048 | 0.043 | 0.000786 | 0.000785 | 0.858 | 0.909 |
| All | M.half-sessions | ips_ratio | 180 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.954 | no | 0.030 | 0.025 | 0.158 | 0.157 | 1.000 | 0.946 |
| Women's | H.half-long | ips | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.947 | no | 0.036 | 0.026 | 0.00126 | 0.00125 | 0.964 | 0.937 |
| Women's | M.half-sessions | ips | impressions | 0.919 | 0.910 to 0.927 | unresolved | no | 0.910 | no | 0.043 | 0.038 | 0.00081 | 0.00081 | 0.883 | 0.918 |
| Women's | H.two-level | snips_ratio | 180 min | 0.932 | 0.924 to 0.940 | unresolved | no | 0.942 | no | 0.044 | 0.023 | 0.231 | 0.229 | 0.960 | 0.935 |
| All | H.half-long | ips_ratio | 180 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.949 | no | 0.032 | 0.028 | 0.191 | 0.19 | 0.984 | 0.941 |
| All | H.half-long | snips_ratio | 180 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.948 | no | 0.034 | 0.028 | 0.19 | 0.189 | 0.976 | 0.939 |
| All | F | ips | 10 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.953 | no | 0.035 | 0.021 | 0.000718 | 0.000715 | 0.996 | 0.945 |
| Women's | FH | v_on | 60 min | 0.888 | 0.878 to 0.897 | under-covers | no | 0.897 | no | 0.062 | 0.050 | 0.000659 | 0.000656 | 0.814 | 0.888 |
| Women's | H.two-level | ips_ratio | 180 min | 0.934 | 0.926 to 0.941 | adequate | no | 0.943 | no | 0.044 | 0.021 | 0.233 | 0.23 | 0.965 | 0.936 |
| All | M.double-sessions | v_on | 60 min | 0.956 | 0.949 to 0.962 | adequate | yes | 0.966 | no | 0.024 | 0.020 | 0.000181 | 0.00018 | 1.066 | 0.957 |
| Women's | F | v_on | 180 min | 0.957 | 0.950 to 0.962 | adequate | yes | 0.966 | no | 0.024 | 0.020 | 0.000254 | 0.000253 | 1.051 | 0.957 |
| All | F | ips | impressions | 0.910 | 0.901 to 0.919 | under-covers | no | 0.920 | no | 0.052 | 0.037 | 0.000634 | 0.000633 | 0.879 | 0.911 |
| Women's | M.two-level | ips_ratio | 180 min | 0.944 | 0.936 to 0.951 | adequate | yes | 0.953 | no | 0.032 | 0.025 | 0.169 | 0.169 | 0.999 | 0.943 |
| Women's | H.two-level | ips | 180 min | 0.934 | 0.926 to 0.942 | adequate | no | 0.943 | no | 0.044 | 0.021 | 0.00142 | 0.00141 | 0.967 | 0.935 |
| Women's | FH | ips_ratio | 180 min | 0.934 | 0.926 to 0.942 | adequate | no | 0.943 | no | 0.032 | 0.033 | 0.204 | 0.203 | 0.957 | 0.935 |
| All | H.two-level | snips_ratio | 180 min | 0.939 | 0.931 to 0.946 | adequate | no | 0.948 | no | 0.035 | 0.027 | 0.191 | 0.19 | 0.976 | 0.938 |
| Women's | H.half-long | ips_ratio | 180 min | 0.938 | 0.930 to 0.945 | adequate | no | 0.947 | no | 0.033 | 0.029 | 0.204 | 0.203 | 0.962 | 0.938 |
| All | M.double-sessions | ips_ratio | 180 min | 0.945 | 0.937 to 0.952 | adequate | yes | 0.954 | no | 0.029 | 0.026 | 0.167 | 0.167 | 1.000 | 0.946 |
| Women's | M.two-level | ips | 180 min | 0.944 | 0.937 to 0.951 | adequate | yes | 0.953 | no | 0.032 | 0.024 | 0.00105 | 0.00104 | 1.004 | 0.943 |
| All | FH | ips_ratio | 180 min | 0.942 | 0.934 to 0.949 | adequate | no | 0.950 | no | 0.030 | 0.028 | 0.17 | 0.169 | 0.975 | 0.940 |
| Women's | F | snips_ratio | 180 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.951 | no | 0.032 | 0.025 | 0.137 | 0.136 | 0.992 | 0.943 |
| All | FS | ips_ratio | 180 min | 0.969 | 0.963 to 0.974 | adequate | no | 0.977 | no | 0.015 | 0.017 | 0.167 | 0.166 | 1.135 | 0.969 |
| Women's | M.half-sessions | ips_ratio | 180 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.954 | no | 0.030 | 0.025 | 0.151 | 0.15 | 1.032 | 0.946 |
| All | F | ips_ratio | 10 min | 0.945 | 0.937 to 0.951 | adequate | yes | 0.953 | no | 0.033 | 0.022 | 0.148 | 0.147 | 0.994 | 0.945 |
| All | F | snips_ratio | 60 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.951 | no | 0.034 | 0.024 | 0.146 | 0.145 | 0.982 | 0.942 |
| All | H.double-long | ips | 180 min | 0.940 | 0.932 to 0.947 | adequate | no | 0.948 | no | 0.032 | 0.028 | 0.000925 | 0.000919 | 0.969 | 0.940 |
| All | H.two-level | v_on | 60 min | 0.931 | 0.922 to 0.938 | unresolved | no | 0.939 | no | 0.035 | 0.034 | 0.000225 | 0.000224 | 0.935 | 0.931 |
| All | F | ips | 30 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.954 | no | 0.034 | 0.020 | 0.00072 | 0.000718 | 0.999 | 0.947 |
| All | F | ips | 60 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.954 | no | 0.035 | 0.020 | 0.000718 | 0.000715 | 0.996 | 0.945 |
| All | FS | snips_ratio | 180 min | 0.968 | 0.962 to 0.973 | adequate | no | 0.976 | no | 0.015 | 0.017 | 0.166 | 0.165 | 1.126 | 0.968 |
| All | F | ips_ratio | 30 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.034 | 0.020 | 0.148 | 0.148 | 0.999 | 0.946 |
| Women's | F | ips_ratio | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.955 | no | 0.030 | 0.022 | 0.139 | 0.139 | 1.010 | 0.947 |
| All | M.double-sessions | snips_ratio | 180 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.952 | no | 0.030 | 0.027 | 0.166 | 0.165 | 0.991 | 0.943 |
| Women's | M.double-sessions | snips_ratio | 180 min | 0.943 | 0.935 to 0.950 | adequate | no | 0.951 | no | 0.029 | 0.029 | 0.169 | 0.168 | 0.988 | 0.943 |
| All | M.half-sessions | v_on | 180 min | 0.975 | 0.970 to 0.980 | unresolved | no | 0.983 | no | 0.015 | 0.010 | 0.000188 | 0.000187 | 1.183 | 0.975 |
| Women's | H.half-long | snips_ratio | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.945 | no | 0.033 | 0.030 | 0.203 | 0.202 | 0.955 | 0.937 |
| All | H.half-long | v_on | 180 min | 0.958 | 0.951 to 0.963 | adequate | no | 0.965 | no | 0.023 | 0.019 | 0.000245 | 0.000244 | 1.060 | 0.959 |
| Women's | M.double-sessions | ips | 180 min | 0.945 | 0.937 to 0.952 | adequate | yes | 0.953 | no | 0.031 | 0.024 | 0.00106 | 0.00105 | 1.006 | 0.945 |
| Women's | M.half-sessions | v_on | 5 min | 0.949 | 0.942 to 0.956 | adequate | yes | 0.941 | no | 0.023 | 0.028 | 0.000194 | 0.000194 | 0.990 | 0.949 |
| All | F | snips_ratio | 10 min | 0.942 | 0.934 to 0.949 | adequate | no | 0.950 | no | 0.035 | 0.023 | 0.145 | 0.145 | 0.979 | 0.942 |
| All | H.half-long | ips | 180 min | 0.941 | 0.933 to 0.948 | adequate | no | 0.949 | no | 0.035 | 0.024 | 0.000919 | 0.000916 | 0.983 | 0.941 |
| Women's | F | ips | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.955 | no | 0.031 | 0.022 | 0.000852 | 0.000849 | 1.017 | 0.948 |
| All | S | v_on | impressions | 0.943 | 0.935 to 0.949 | adequate | no | 0.950 | no | 0.027 | 0.030 | 7.81e-05 | 7.81e-05 | 0.986 | 0.943 |
| All | FH | snips_ratio | 180 min | 0.941 | 0.933 to 0.947 | adequate | no | 0.948 | no | 0.030 | 0.029 | 0.168 | 0.167 | 0.966 | 0.939 |
| All | F | ips_ratio | 20 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.033 | 0.021 | 0.148 | 0.148 | 0.996 | 0.946 |
| All | F | ips_ratio | 60 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.033 | 0.020 | 0.148 | 0.148 | 0.997 | 0.946 |
| All | M.double-sessions | ips | 180 min | 0.945 | 0.937 to 0.952 | adequate | yes | 0.952 | no | 0.031 | 0.024 | 0.000808 | 0.000803 | 0.997 | 0.945 |
| Women's | M.half-sessions | ips | 180 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.954 | no | 0.031 | 0.022 | 0.000937 | 0.000931 | 1.023 | 0.946 |
| Women's | H.double-long | v_on | 180 min | 0.937 | 0.929 to 0.944 | adequate | no | 0.944 | no | 0.035 | 0.027 | 0.00045 | 0.000447 | 0.966 | 0.936 |
| All | F | ips | 5 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.035 | 0.019 | 0.000719 | 0.000718 | 0.998 | 0.947 |
| All | S | ips | 180 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.954 | no | 0.030 | 0.022 | 0.000627 | 0.000623 | 1.005 | 0.947 |
| All | FS | ips | 180 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.028 | 0.026 | 0.00071 | 0.000705 | 0.994 | 0.947 |
| Women's | M.two-level | v_on | 180 min | 0.958 | 0.951 to 0.963 | adequate | no | 0.965 | no | 0.026 | 0.017 | 0.000265 | 0.000263 | 1.059 | 0.957 |
| Men's | F | ips_ratio | 10 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.034 | 0.021 | 0.169 | 0.169 | 1.005 | 0.946 |
| All | H.two-level | ips | 180 min | 0.942 | 0.934 to 0.948 | adequate | no | 0.949 | no | 0.034 | 0.024 | 0.000923 | 0.000917 | 0.985 | 0.941 |
| All | F | snips_ratio | 5 min | 0.942 | 0.935 to 0.949 | adequate | no | 0.949 | no | 0.035 | 0.023 | 0.145 | 0.145 | 0.980 | 0.943 |
| All | F | snips_ratio | 30 min | 0.944 | 0.936 to 0.950 | adequate | yes | 0.950 | no | 0.035 | 0.021 | 0.146 | 0.145 | 0.982 | 0.943 |
| All | F | v_on | 180 min | 0.980 | 0.975 to 0.984 | unresolved | no | 0.987 | no | 0.012 | 0.009 | 0.000176 | 0.000176 | 1.249 | 0.980 |
| Women's | M.two-level | ips | 60 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.032 | 0.022 | 0.00106 | 0.00105 | 1.010 | 0.946 |
| All | M.half-sessions | ips | 180 min | 0.946 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.030 | 0.024 | 0.000761 | 0.000759 | 0.994 | 0.945 |
| Men's | F | ips_ratio | 60 min | 0.947 | 0.940 to 0.954 | adequate | yes | 0.954 | no | 0.032 | 0.021 | 0.169 | 0.169 | 1.008 | 0.947 |
| All | F | ips_ratio | 5 min | 0.946 | 0.938 to 0.952 | adequate | yes | 0.953 | no | 0.033 | 0.021 | 0.148 | 0.147 | 0.994 | 0.946 |
| Men's | F | v_on | 60 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.029 | 0.025 | 0.000337 | 0.000336 | 0.997 | 0.948 |
| All | FS | ips_ratio | 20 min | 0.952 | 0.944 to 0.958 | adequate | yes | 0.958 | no | 0.025 | 0.024 | 0.151 | 0.151 | 1.026 | 0.952 |
| Men's | F | ips | 10 min | 0.947 | 0.939 to 0.953 | adequate | yes | 0.953 | no | 0.034 | 0.020 | 0.00109 | 0.00109 | 1.005 | 0.947 |
| All | F | v_on | 60 min | 0.964 | 0.958 to 0.970 | adequate | no | 0.971 | no | 0.019 | 0.017 | 0.000158 | 0.000158 | 1.118 | 0.964 |
| All | M.two-level | v_on | 180 min | 0.976 | 0.970 to 0.980 | unresolved | no | 0.981 | no | 0.015 | 0.010 | 0.000197 | 0.000196 | 1.165 | 0.974 |
| All | S | snips_ratio | 180 min | 0.971 | 0.966 to 0.976 | unresolved | no | 0.976 | no | 0.016 | 0.013 | 0.145 | 0.144 | 1.142 | 0.972 |
| All | S | ips_ratio | 180 min | 0.973 | 0.968 to 0.978 | unresolved | no | 0.978 | no | 0.015 | 0.013 | 0.146 | 0.146 | 1.154 | 0.973 |
| Women's | FS | v_on | 5 min | 0.971 | 0.966 to 0.976 | unresolved | no | 0.976 | no | 0.015 | 0.014 | 0.000285 | 0.000285 | 1.136 | 0.972 |
| Women's | S | snips_ratio | 180 min | 0.992 | 0.988 to 0.994 | over-covers | no | 0.994 | no | 0.004 | 0.004 | 0.173 | 0.173 | 1.386 | 0.992 |
| All | S | v_on | 5 min | 0.989 | 0.986 to 0.992 | over-covers | no | 0.992 | no | 0.006 | 0.004 | 0.000105 | 0.000105 | 1.327 | 0.989 |
| Women's | FS | snips_ratio | 180 min | 0.992 | 0.988 to 0.994 | over-covers | no | 0.994 | no | 0.003 | 0.005 | 0.192 | 0.191 | 1.394 | 0.991 |
| Women's | FS | ips_ratio | 180 min | 0.993 | 0.989 to 0.995 | over-covers | no | 0.995 | no | 0.004 | 0.004 | 0.195 | 0.194 | 1.415 | 0.993 |
| Women's | S | ips_ratio | 180 min | 0.993 | 0.990 to 0.995 | over-covers | no | 0.995 | no | 0.004 | 0.004 | 0.176 | 0.176 | 1.411 | 0.993 |
| All | S | v_on | 10 min | 0.997 | 0.995 to 0.998 | over-covers | no | 0.999 | no | 0.002 | 0.002 | 0.000127 | 0.000127 | 1.617 | 0.997 |
