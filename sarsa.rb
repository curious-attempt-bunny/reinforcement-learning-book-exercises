# Exercise 6.7: Windy gridworld with kings' moves -- page 136

# Initialize Q(s,a) arbitrarily
q = Hash.new { |hash, key| hash[key] = 0 }

a_all = [
    {x: -1, y: -1},{x: 0, y: -1},{x: 1, y: -1},
    {x: -1, y: 0},{x: 1, y: 0},
    {x: -1, y: 1},{x: 0, y: 1},{x: 1, y: 1}
]

a_all << {x: 0, y: 0} # A ninth action that causes no movement at all other than that caused by the wind?

y_wind = [0,0,0,1,1,1,2,2,1,0]
goal = {x: 7, y: 3}

alpha = 0.5
gamma = 1.0 # undiscounted
episilon = 0.1

def episilon_greedy_policy(q, a_all, episilon, s)
    if rand() > episilon
        a_all.max_by { |a| q["#{s}-#{a}"] }
    else
        a_all.sample
    end
end

1.upto(200) do |episode|
    # use this to for convergence to the optimum (page 135):
    # episilon = 1.0 / episode 

    # Initialize S
    s = {x: 0, y: 3}
    # Choose A from S using policy derived from Q (e.g. episilon-greedy)
    a = episilon_greedy_policy(q, a_all, episilon, s)

    episode_length = 0
    while true
        episode_length += 1
        # Take action A, observe R, S'
        s_next = s.dup
        s_next[:x] += a[:x]
        s_next[:x] = 0 if s_next[:x] < 0
        s_next[:x] = y_wind.size-1 if s_next[:x] == y_wind.size
        
        s_next[:y] += a[:y]
        s_next[:y] -= y_wind[s[:y]]
        s_next[:y] = 0 if s_next[:y] < 0
        s_next[:y] = 6 if s_next[:y] > 6

        r = -1

        # Choose A' from S' using policy derived from Q (e.g. episilon-greedy)
        a_next = episilon_greedy_policy(q, a_all, episilon, s_next)

        # Q(S,A) <-- Q(S,A) + alpha*(R + gamma*Q(S',A') - Q(S,A))
        q["#{s}-#{a}"] = q["#{s}-#{a}"] + alpha*(r + gamma*q["#{s_next}-#{a_next}"] - q["#{s}-#{a}"])
        
        # S <-- S'; A <-- A'
        s = s_next
        a = a_next

        break if s[:x] == goal[:x] && s[:y] == goal[:y]
    end

    puts "#{episode}: #{'#'*episode_length}"
end