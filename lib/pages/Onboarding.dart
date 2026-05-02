import 'package:flutter/material.dart';

class Onboarding extends StatefulWidget {
  const Onboarding({super.key});

  @override
  State<Onboarding> createState() => _OnboardingState();
}

class _OnboardingState extends State<Onboarding> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8EDC2),
      body: Stack(
        children: [
          // 1. Top Section for Image
          Column(
            children: [
              const SizedBox(height: 80.0),
              Center(
                child: Image.asset(
                  'images/onboard.png',
                  height: 350,
                  fit: BoxFit.contain,
                ),
              ),
            ],
          ),
          // 2. White Bottom Sheet Container
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height / 2.3,
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(40),
                  topRight: Radius.circular(40),
                ),
              ),
              child: Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 30.0,
                  vertical: 40.0,
                ),
                child: Column(
                  children: [
                    const Text(
                      "Manage your daily \nlife expenses",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 32.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 20),
                    const Text(
                      "Expense Tracker is a simple and efficient personal finance management app that allows you to track your daily expenses and income",
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.black54, fontSize: 16.0),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
