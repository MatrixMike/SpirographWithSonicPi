#spiro.rb
#Spirograph controlled by Sonic Pi written by Robin Newman, December 2018
use_debug false
use_osc_logging false
use_cue_logging false
use_osc "localhost",8000
define :scx do |n,r| #get note to play based on circle radius r and x coordinate n
  return scale(:c4,:major,num_octaves: 2)[(n.abs/r.to_f*15).to_int]
end

define :scy do |n,r| #get selection index based on circle radius r and y coordinate n
  return (n.abs/r.to_f*4).to_i
end

set :v,1 #initial volume index value

#p contains data list for 7 drawings
p=[["250","105","175","purple","saw"],["300","187","203","yellow","tri"],
   ["300","103","201","blue","sine"],["322","63","87","purple","tri"],
   ["309","351","300","forest green","saw"],["272","107","109","cyan","pulse"],
   ["180","67","100","red","piano"]]

#main control thread to start each drawing, then wait for drawing to finish
in_thread do
  p.length.times do |x|
    set :r,p[x][0] #store large circle radius
    set :s,p[x][4] #store current synth
    osc "/draw",p[x][0],p[x][1],p[x][2],p[x][3] #ssend data for next drawing
    b = sync "/osc*/finished" #wait for drawing to finish
  end
end


#Playing section. Responds to OSC messages from spirograph.py
with_fx :reverb do
  live_loop :plx do
    use_real_time
    n = sync "/osc*/xcoord" #use osc* so works with SP 3.1 and 3.2dev
    use_transpose [-17,-12,0,7,12,19][get(:v)]
    synth get(:s),note: scx(n[0],get(:r)),attack: 0.05,release: 0.2,pan: [-0.8,0.8].choose,amp: [0.3,0.5,0.7,0.8,1][get(:v)]
  end
  live_loop :ply do
    use_real_time
    n = sync "/osc*/ycoord" #trigger sample when y coord received
    i = scy(n[0],get(:r))
    set :v,i #adjust volume for plx loop
    sample sample_names([:drum,:elec].choose ).choose,amp: 2,pan: [-1,0,1].choose
  end
end
