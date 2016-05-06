# Exercise 4.9 (page 89)

probability_heads = 0.4

vee = [0]*100
vee[0] = 0
vee[100] = 1

S = (1..99).to_a
theta = 0.00001

iteration = 1
while true
    delta = 0

    next_vee = vee.dup
    S.each do |s|
        next_vee[s] = 1.upto([s, 100-s].min).map do |a|
            probability_heads*vee[s+a] + (1-probability_heads)*vee[s-a]
        end.max
        delta = [delta,(vee[s] - next_vee[s]).abs].max
    end
    vee = next_vee

    puts "Iteration #{iteration} has delta #{delta}"
    iteration += 1

    break if delta < theta
end

S.each do |s|
    a = 1.upto([s, 100-s].min).max_by do |a|
        probability_heads*vee[s+a] + (1-probability_heads)*vee[s-a]
    end
    puts "#{s}: #{'#'*a} (#{a})"
end