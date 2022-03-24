# for init in 1897-01-{16T22,16T04,17T00,15T22,16T16,16T10,15T04} 1926-07-{30T15,30T13,30T07,30T01,29T19,29T13,28T19}
for init in 1897-01-{16T22,16T04,15T04} 1926-07-{30T13,29T19,28T19}
do

ffmpeg -y -framerate 24 -pattern_type glob -i "./animation-figs/*${init}*.png" -c:v libx264 -pix_fmt yuv420p -vf scale=-2:720 "./animations/lorenz63_schema_init_${init}.mp4"

done
