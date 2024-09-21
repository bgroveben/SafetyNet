To calculate the position and speed of a fixed-wing UAV as it taxis back and forth between two points on the runway, you'll need to use some basic principles of kinematics and measurements. Here's a step-by-step guide on how to do it:

1.  **Define the two points**: Determine the coordinates of the two points on the runway where the UAV will be taxiing back and forth. Let's call these points Point A (initial position) and Point B (destination position).
    
2.  **Collect data**: For accurate calculations, you'll need to gather data from the UAV during its taxiing. This data may include timestamps, GPS coordinates, and any other relevant measurements.
    
3.  **Calculate distance**: Use the GPS coordinates (latitude and longitude) of Point A and Point B to calculate the distance between them. You can use the Haversine formula or other distance calculation methods that take into account the curvature of the Earth.
    
4.  **Measure time**: Record the time it takes for the UAV to taxi from Point A to Point B and back to Point A.
    
5.  **Calculate speed**: Use the distance calculated in step 3 and the time measured in step 4 to find the average speed of the UAV during its taxiing.
    
    Speed (m/s) = Distance (m) / Time (s)
    
6.  **Calculate position**: To track the UAV's position as it moves between the two points, you can use the concept of linear interpolation. Linear interpolation is a method to estimate a value (in this case, the UAV's position) within a range of two known values (Point A and Point B) based on a proportion of the distance traveled.
    
    Let:
    
    -	d_total = total distance between Point A and Point B (calculated in step 3).
    -   d_current = distance covered by the UAV from Point A (measured during taxiing).
    -   proportion = d_current / d_total
    
    The UAV's current position (latitude and longitude) can be calculated as:
    
    -   Latitude_current = Latitude_A + proportion * (Latitude_B - Latitude_A)
    -   Longitude_current = Longitude_A + proportion * (Longitude_B - Longitude_A)
    
    Note: Make sure to use radians instead of degrees when performing calculations involving latitude and longitude.
    
7.  Repeat steps 4 to 6: Continuously collect data, measure time, calculate speed, and update the UAV's position as it taxis back and forth between the two points.
    
Keep in mind that the accuracy of these calculations will depend on the precision of your data collection methods and the accuracy of the GPS measurements. Also, ensure the UAV is operating in an open area with a clear line of sight to multiple GPS satellites for accurate positioning.