#include "GLFW\glfw3.h"
#include "imgui.h"
#include "imgui_impl_opengl3.h"
#include "imgui_impl_dx9.h"
#include "imgui_impl_win32.h"
#include <iostream>


int main() {
// Inside your setup function
IMGUI_CHECKVERSION();
ImGui::CreateContext();
ImGuiIO &io = ImGui::GetIO(); (void)io;
ImGui::StyleColorsDark(); // Choose a default theme

// Initialize the backend (e.g., OpenGL)
ImGui_ImplOpenGL3_Init("#version 150"); // Set the appropriate version for your graphics library

GLFWwindow* window = glfwCreateWindow(800, 600, "My Window", NULL, NULL);
if (window == NULL)
{
    std::cout << "Failed to create GLFW window" << std::endl;
    glfwTerminate();
    return -1;
}
glfwMakeContextCurrent(window);

while (!glfwWindowShouldClose(window)) // Replace with your window loop condition
{
    glfwPollEvents(); // Poll events for your windowing system

    ImGui_ImplOpenGL3_NewFrame(); // New frame for the backend
    ImGui::NewFrame();

    // ImGui code goes here
    ImGui::Begin("My First ImGui Window");

    if (ImGui::Button("Click me!"))
    {
        // Respond to button click
        std::cout << "Button clicked!" << std::endl;
    }

    static float slider_value = 0.0f;
    ImGui::SliderFloat("Slider", &slider_value, 0.0f, 100.0f);

    ImGui::End();

    ImGui::Render();
    int display_w, display_h;
    glfwGetFramebufferSize(window, &display_w, &display_h);
    glViewport(0, 0, display_w, display_h);
    glClear(GL_COLOR_BUFFER_BIT);
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

    glfwSwapBuffers(window); // Swap buffers for your windowing system
}

ImGui_ImplOpenGL3_Shutdown(); // Shutdown the backend
ImGui::DestroyContext();

return 0;
}







