#spiroAuto.rb
#Spirograph controlled by Sonic Pi written by Robin Newman, December 2018
#requires release 2 version of supporting python files
#this version allows program to rerun and start a new drawing
#before the current drawing finishes. Also support random colour selection
#and random selection of drawing parameters
use_debug false
use_osc_logging false
use_cue_logging false

use_osc "localhost",8000
osc "/kill","finished"

sleep 1


define :scx do |n,r| #get note to play based on circle radius r and x coordinate n
  return scale(:c4,:major,num_octaves: 2)[(n.abs/r.to_f*15).to_int]
end

define :scy do |n,r| #get selection index based on circle radius r and y coordinate n
  return (n.abs/r.to_f*4).to_i
end

set :v,1 #intial volume index value

#main control thread to start each drawing, then wait for drawing to finish
live_loop :spiro do
  t = Time.now.to_i
  use_random_seed t
  p=[rrand_i(90,140).to_s,rrand_i(170,220).to_s,rrand_i(260,310).to_s].shuffle
  
  #p contains data list for 7 drawings
  p+=[["purple","red","yellow","green","blue"].choose,["saw","tri","piano"].choose,
      ["true","false","false","false"].choose]
  
  set :r,p[0] #store large circle radius
  set :s,p[4] #store current synth
  osc "/draw",p[0],p[1],p[2],p[3],p[5] #ssend data for next drawing
  b = sync "/osc*/finished" #wait for drawing to finish
end


#Playing section. Responds to OSC messages from spirograph.py
with_fx :reverb do
  live_loop :plx do
    use_real_time
    n = sync "/osc*/xcoord" #use osc* so works with SP 3.1 and 3.2dev
    use_transpose [-17,-12,0,7,12,19][[get(:v),5].min]
    synth get(:s),note: scx(n[0],get(:r)),attack: 0.05,release: 0.2,pan: [-0.8,0.8].choose,amp: [0.3,0.5,0.7,0.8,1][get(:v)]
  end
  live_loop :ply do
    use_real_time
    n = sync "/osc*/ycoord" #trigger sample when y coord received
    i = scy(n[0],get(:r))
    puts i
    set :v,i #adjust volume for plx loop
    sample sample_names([:drum,:elec].choose ).choose,amp: 0.4,pan: [-1,0,1].choose
  end
end
