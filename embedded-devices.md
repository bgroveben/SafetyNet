When working with embedded systems, especially in real-time and safety-critical applications, there are several concerns beyond latency that should be carefully considered:

1. **Power Consumption:**
   - Embedded devices often have power constraints, particularly in applications like UAVs. Balancing functionality with power efficiency is crucial for extended operation and overall system performance.

2. **Memory Usage:**
   - Limited memory resources can impact the ability to store and process data. Optimize code and consider the memory requirements of algorithms and data structures.

3. **Processing Power:**
   - The processing capabilities of the embedded device must match the computational demands of the application. Insufficient processing power can lead to delays and reduced system performance.

4. **Reliability and Redundancy:**
   - In safety-critical applications, reliability is paramount. Consider incorporating redundancy or failover mechanisms to ensure continued operation in the event of component failure.

5. **Environmental Conditions:**
   - Embedded systems may operate in harsh environments. Ensure that the chosen devices can withstand temperature variations, humidity, vibrations, and other environmental factors.

6. **Regulatory Compliance:**
   - Adherence to industry standards and regulations is critical, especially in fields like aerospace and medical devices. Compliance ensures that the system meets safety and reliability requirements.

7. **Security:**
   - Embedded systems can be vulnerable to security threats. Implement secure communication protocols, encryption, and access controls to protect against unauthorized access and data breaches.

8. **Integration with Sensors and Actuators:**
   - Ensure that the embedded system can seamlessly integrate with sensors and actuators, as they are critical components for sensing the environment and effecting control.

9. **Scalability:**
   - Consider whether the system can be easily scaled to accommodate additional features or components. This is particularly important for projects with evolving requirements.

10. **Real-Time Operating System (RTOS):**
    - Choosing the right RTOS is crucial for systems with real-time requirements. The RTOS should provide deterministic behavior, scheduling capabilities, and support for time-critical tasks.

11. **Software Development Tools:**
    - Availability of robust development tools, compilers, and debugging support is essential for efficient software development and troubleshooting.

12. **Long-Term Availability:**
    - Ensure that the selected embedded device or components will be available for the duration of the project. Long-term availability is crucial for maintenance and upgrades.

13. **Cost:**
    - Evaluate the overall cost of the embedded system, including hardware, software development, and maintenance. Consider both upfront costs and long-term expenses.

14. **Ease of Maintenance and Upgrades:**
    - Design the system with maintenance in mind. Ensure that software updates and hardware upgrades can be performed efficiently without significant disruptions.

15. **Interoperability:**
    - If the embedded system needs to interact with other systems or devices, ensure compatibility and interoperability with existing standards and protocols.

Considering these concerns holistically during the design and development phases will contribute to the successful implementation of embedded systems, especially in applications where performance, reliability, and real-time capabilities are critical.